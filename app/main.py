from fastapi import FastAPI, HTTPException
from .schemas import OrchestratorRequest, NoteMakerInput, FlashcardInput, ConceptExplainerInput
from .tool_registry import register_tool
from .tools.mock_note_maker import generate_notes
from .tools.mock_flashcard import generate_flashcards
from .tools.mock_concept_explainer import explain_concept
from .orchestrator import orchestrate, OrchestrationError

app = FastAPI(title="Autonomous AI Tutor Orchestrator")

# register tools (names chosen to match orchestrator)
register_tool("note_maker", NoteMakerInput, generate_notes)
register_tool("flashcard_generator", FlashcardInput, generate_flashcards)
register_tool("concept_explainer", ConceptExplainerInput, explain_concept)

@app.post("/orchestrate")
async def run_orchestrator(req: OrchestratorRequest):
    try:
        result = orchestrate(req)
        return result
    except OrchestrationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

