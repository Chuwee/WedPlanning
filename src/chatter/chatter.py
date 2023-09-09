import openai  # Import the OpenAI library
import os  # Import the os library
import json  # Import the json library


class Chatter:
    def __init__(self, db) -> None:
        self.db = db
        openai.api_key = open(os.getcwd() + "/whisperer/api_key.txt", "r").read()

    def new_guest(self, name, age, groupname):
        db = self.db
        if name == "done" or age == "done" or groupname == "done":
            return "done"
        db.add_guest([name, age, groupname])
        return (
            "Added guest "
            + name
            + " to group "
            + groupname
            + '! Keep going or type "done" to finish.'
        )

    def extract_transcript_whisper(self):
        transcript = os.open(os.getcwd() + "/transcript.txt", os.O_RDONLY)
        transcript = str(os.read(transcript, 1024))
        return transcript

    def run_conversation(self):
        transcript = self.extract_transcript_whisper()
        first_prompt = os.open(os.getcwd() + "/chatter/prompt.txt", os.O_RDONLY)
        first_prompt = str(os.read(first_prompt, 2048))
        # Step 1: send the conversation and available functions to GPT
        messages = [
            {"role": "system", "content": first_prompt},
            {"role": "user", "content": transcript},
        ]
        functions = [
            {
                "name": "new_guest",
                "description": "Adds a guest to the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                        "type": "string",
                        "description": "Name of the guest to be added",
                        },
                        "age": {
                            "type": "integer",
                            "description": "Age of the guest to be added",
                        },
                        "groupname": {
                            "type": "string",
                            "description": 'The group name of the guest, for example "Smith Family" or "Coworker"',
                        },
                    },
                    "required": ["name", "age", "groupname"],
                },
            }
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",  # auto is default, but we'll be explicit
        )
        response_message = response["choices"][0]["message"]
        while response_message.get("function_call"):
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "new_guest": self.new_guest,
            }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = fuction_to_call(
                name=function_args.get("name"),
                age=function_args.get("age"),
                groupname=function_args.get("groupname"),
            )
            # Step 4: send the info on the function call and function response to GPT
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
                functions=functions,
                function_call="auto",  # auto is default, but we'll be explicit
            )
            response_message = response["choices"][0]["message"]

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return messages
