from utils.google_docs import create_doc_in_folder

if __name__ == "__main__":
    print("🚀 Attempting to create Google Doc...")
    doc_id = create_doc_in_folder("RSS WWR Job Feed")
    print(f"✅ Document created with ID: {doc_id}")
