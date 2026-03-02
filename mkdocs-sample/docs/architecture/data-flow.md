# Data Flow & User Experience

This page demonstrates **visual evidence** with real UI screenshots and feature demos.

## Chat Interface

![Chat Interface](../assets/docs-images/chat-interface.png)

**Key Features**: Real-time streaming, citation highlighting, session management, multilingual support.

## Document Upload Workflow

### Pre-Upload
![Upload Pre-Upload](../assets/docs-images/manage-content-upload-files.png)

### In Progress
![Upload Uploading](../assets/docs-images/manage-content-upload-status.png)

### Complete
![Upload Uploaded](../assets/docs-images/view-upload-status-link.png)

**Pipeline**: Frontend -> Blob -> Azure Function -> OCR -> Chunking -> Embedding -> Search Index

## Content Management

![Content Library](../assets/docs-images/manage-content-interface.png)

**Capabilities**: Browse documents, filter, delete, preview metadata.

## Feature Demonstrations

### Math Assistant
![Math Assistant](../assets/docs-images/math-assistant-ui.png)

### Data Assist
![Data Assist](../assets/docs-images/tab-data-assist-upload-files-ui.png)

### Citation Modal
![Citation Modal](../assets/docs-images/UX_anlysispanel_citation_document.png)

### Thought Process Viewer
![Thought Process](../assets/docs-images/UX_analysispanel_thoughtprocess.png)

## Governance

![Analysis Panel](../assets/docs-images/UX_analysispanel_supportingcontent.png)

## Code Example

``` python
async def chat_endpoint(message: str, session_id: str):
    optimized_query = await ai_services.optimize_query(message)
    query_embedding = await enrichment.generate_embedding(optimized_query)
    results = await search.hybrid_search(text=optimized_query, vector=query_embedding, top_k=8)
    context = format_context(results)
    async for chunk in openai.chat_stream(system_prompt=SYSTEM_PROMPT, user_message=message, context=context):
        yield chunk
    await cosmos.log_conversation(session_id, message, response)
```

---

**Asset Source**: Real UI screenshots from EVA-JP-reference local repository
