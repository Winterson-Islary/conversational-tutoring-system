"""For converting PDF to Markdown with image annotations"""

import os
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    PictureDescriptionApiOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.base import ImageRefMode
from dotenv import load_dotenv
from langchain_text_splitters import MarkdownHeaderTextSplitter

from config import config

load_dotenv()
MARKDOWN_HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]


def chunk_markdown_by_headers(inputMarkdownDocument: str):
    markdownSplitter = MarkdownHeaderTextSplitter(
        MARKDOWN_HEADERS_TO_SPLIT_ON, strip_headers=False
    )
    return markdownSplitter.split_text(inputMarkdownDocument)


def convert_doc_with_image_annotation(inputDocumentPath):
    api_key = os.environ.get("GROQ_API_KEY")
    model = config["services"]["image_annotation"]["model"]
    api_url = config["services"]["image_annotation"]["url"]
    pictureDescriptionApiOption = PictureDescriptionApiOptions(
        url=api_url,
        prompt="Describe this image in sentences in a single paragraph.",
        params=dict(model=model),
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )

    pipelineOptions = PdfPipelineOptions(
        do_picture_description=True,
        picture_description_options=pictureDescriptionApiOption,
        enable_remote_services=True,
        generate_picture_images=True,
        images_scale=2,
    )

    docConverter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipelineOptions)
        }
    )
    return docConverter.convert(inputDocumentPath)


def export_to_md_with_image_ref(markdownWithAnnotation):
    return markdownWithAnnotation.document.export_to_markdown(
        # image_mode=ImageRefMode.EMBEDDED,
        include_annotations=True,
    )
