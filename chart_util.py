import os
import time
from dotenv import load_dotenv
from openai import OpenAI
import log_util

class ChartUtil:
    def __init__(self, user_prompt=""):
        load_dotenv()
        self.log = log_util.LogUtil()
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.chart_out_path = "./static/chart.png"
        self.user_prompt=user_prompt

    def generate_chart(self, message):
        # Prepare the prompt
        ci_prompt = f"Please generate a chart using following data: \n {message} \n Never use the field doc_count in your analysis. This data has been generated with this user query {self.user_prompt}. You need to use it to graph the correct metrics if there is many"  
        print(f"Prompt to generate graph {ci_prompt}")
        try:
            # Create a thread and run the assistant
            thread = self.client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": ci_prompt,
                    }
                ]
            )

            # Run the thread
            run = self.client.beta.threads.runs.create(
                assistant_id=os.environ["OPENAI_ASSISTANT_ID"], thread_id=thread.id
            )

            # Poll the run status until it is completed
            while True:
                # Refresh the run to get the latest status
                run = self.client.beta.threads.runs.retrieve(
                    run_id=run.id, thread_id=thread.id
                )

                if run.status == "completed":
                    self.log.info("Generated chart, Run finished")

                    # Get list of messages in the thread
                    messages = self.client.beta.threads.messages.list(
                        thread_id=thread.id
                    )

                    # Get the latest message in the thread and retrieve file id
                    self.log.info(messages.data[0])
                    image_file_id = messages.data[0].content[0].image_file.file_id
                    content_description = messages.data[0].content[1].text.value

                    # Get the raw response from the file id
                    raw_response = self.client.files.with_raw_response.content(
                        file_id=image_file_id
                    )

                    # Delete generated file
                    self.client.files.delete(image_file_id)

                    # Save the generated chart to a file
                    with open(self.chart_out_path, "wb") as f:
                        f.write(raw_response.content)
                        return (self.chart_out_path, content_description)

                elif run.status == "failed":
                    self.log.error("Unable to generate chart")
                    break

                # Wait for a short period before polling again to avoid hitting rate limits
                time.sleep(1)
        except Exception as e:
            self.log.error(e)

        return (None, "🤔 Could you please rephrase your query and try again?")