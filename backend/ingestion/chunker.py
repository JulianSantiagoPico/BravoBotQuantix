from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(texto: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    chunks = splitter.split_text(texto)
    return [c.strip() for c in chunks if c.strip()]
