from fastapi import APIRouter, HTTPException, Request, Response
from app.services.search_service import WebSearcher
from app.services.llm_service import LLMProcessor
from app.services.pdf_service import PDFService
from typing import Dict
import os

router = APIRouter()

# Initialize services
searcher = WebSearcher()
llm_processor = LLMProcessor()
pdf_service = PDFService()

@router.post("/api/research")
async def research(request: Request):
    try:
        body = await request.json()
        query = body.get('query')
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
            
        # Get research results
        search_results = await searcher.search_company_info(query)
        if not search_results:
            raise HTTPException(status_code=404, detail="No information found")
            
        # Generate report with query context
        report = await llm_processor.generate_report(str(search_results), query)
        
        return {
            "report": report,
            "sources": [article["url"] for article in search_results["articles"]]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/download-pdf")
async def download_pdf(request: Request):
    try:
        body = await request.json()
        report = body.get('report')
        sources = body.get('sources', [])
        query = body.get('query', 'Research Report')
        
        if not report:
            raise HTTPException(status_code=400, detail="Report content is required")
            
        # Generate PDF using the PDF service with query context
        pdf_buffer = pdf_service.generate_pdf(
            title=f"Research Report: {query}",
            content=report,
            sources=sources
        )
        
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{query.replace(" ", "_")}_report.pdf"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 