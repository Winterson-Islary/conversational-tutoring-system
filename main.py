from src.file_converter import (
    convert_doc_with_image_annotation,
    export_to_md_with_image_ref,
)


def main():
    result = convert_doc_with_image_annotation("docs/test-document-1.pdf")
    print(
        result.document.export_to_markdown(
            mark_annotations=True, include_annotations=True
        )
    )
    export_to_md_with_image_ref(result, "cs")


if __name__ == "__main__":
    main()
