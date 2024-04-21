import gradio as gr
import openai
import docx2txt
import PyPDF2


openai.api_key = "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"  # Replace with your key

def read_text_from_file(file_path):
    # Check the file type and read accordingly
    if file_path.endswith('.docx'):
        text = docx2txt.process(file_path)
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as txt_file:
            text = txt_file.read()

    
    return text

css = """
body {
    background-color: #f4f4f4; /* setting it to light grey */
}
.gradio-chat-message-user {
    color: #007BFF; /* Blue text for user inputs */
}
.gradio-chatbot .message.system {
    color: #FFD700; /*yellow text for chatbot response*/
}
.gradio-chat-message-assistant {
    color: #FFD700; /* Yellow text for chatbot responses */
}
.gradio-chat-message {
    font-size: 16px; /* Larger text for readability */
    padding: 8px; /* Some padding around text messages */
}
"""

with gr.Blocks(css=css) as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    filename = gr.File(file_count='multiple')

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(msg, history,filename):
        history_openai_format = []
        for files in filename:
            file_contents = read_text_from_file(files)
            history_openai_format.append({"role": "user", "content": file_contents })
        
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            if assistant is not None:
                history_openai_format.append({"role": "assistant", "content":assistant})
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=history_openai_format,
            stream=True
        #client = openai(
        #api_key=api_key,)
        #response = client.chat.completions.create(
        #messages=history_openai_format,
        # model="gpt-3.5-turbo" # gpt 3.5 turbo
        #model="gpt-4",
        #model = "gpt-4-1106-preview", #gpt-4 turbo
        #stream = True
        )
        history[-1][1] = ""
        #partial_message = ""
        for chunk in response:
            text = (chunk.choices[0].delta.content)
            if text is not None:
                for character in text:
                        history[-1][1] += character
                        yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [msg, chatbot,filename], chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)
    
demo.queue()
demo.launch()