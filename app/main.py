from fastapi import FastAPI, HTTPException
from .schemas import OrchestratorRequest, NoteMakerInput, FlashcardInput, ConceptExplainerInput
from .tool_registry import register_tool
from .tools.mock_note_maker import note_maker_adapter
from .tools.mock_flashcard import flashcard_adapter
from .tools.mock_concept_explainer import concept_explainer_adapter
from .orchestrator import orchestrate, OrchestrationError

app = FastAPI(title="Autonomous AI Tutor Orchestrator")

# register tools (names chosen to match orchestrator)
register_tool("note_maker", NoteMakerInput, note_maker_adapter)
register_tool("flashcard_generator", FlashcardInput, flashcard_adapter)
register_tool("concept_explainer", ConceptExplainerInput, concept_explainer_adapter)

@app.post("/orchestrate")
async def run_orchestrator(req: OrchestratorRequest):
    try:
        result = orchestrate(req)
        return result
    except OrchestrationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

