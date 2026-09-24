from .improver import ImproverPipeline

pipeline = ImproverPipeline("semantic_axes.json")

meta = {"source": "user"}
text = "このコードの違いを比較して"
dict_paths = []  # Phase1では空でOK

result = pipeline.run(meta, text, dict_paths)
print(result)
