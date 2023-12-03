from openai import OpenAI

base_url = "http://localhost:22222"
api_key = "sk-xxxxx"


client = OpenAI(base_url=base_url, api_key=api_key)

extra_body = {
    "invocation_id": 1,
}

response = client.chat.completions.create(
    model="precise",
    messages=[
        {
            "role": "user",
            "content": "how many questions have I asked you?",
        }
    ],
    stream=True,
    extra_body=extra_body,
)

print(response)

for chunk in response:
    # print(chunk.choices[0].delta)
    print("??")

# print(response.choices[0].message)
# print(response)

# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content)
#     else:
#         print(chunk)
