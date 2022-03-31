def func(text1, text2, number):
    return f"Hello  {text1} {text2}  {number} !!", number + 1


if __name__ == "__main__":
    import gradio as gr

    iface = gr.Interface(fn=func,
                         inputs=["text", "checkbox", gr.inputs.Slider(0, 100)],
                         outputs=["text", "number"],
                         title="emmmmmm",
                         # description=description,
                         # article=article,
                         examples=[["lalala", False, 100], ["emmm", True, 1], ["aaa", True, 101]]
                         )
    iface.launch(debug=True)
