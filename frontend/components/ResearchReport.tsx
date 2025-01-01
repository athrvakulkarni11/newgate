import { Paper, Typography, Button, List, ListItem, Link } from '@mui/material';

interface ResearchReportProps {
  report: string;
  sources: string[];
}

export default function ResearchReport({ report, sources }: ResearchReportProps) {
  const handleDownloadPDF = async () => {
    try {
      // First try to check if the service is available
      const response = await fetch('/api/download-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/pdf',
        },
        body: JSON.stringify({ 
          report,
          sources,
          query: window.sessionStorage.getItem('lastQuery') || 'Research Report',
          filename: 'research-report.pdf'
        }),
      });
      
      // Log the response details regardless of success/failure
      console.log('Server response:', {
        ok: response.ok,
        status: response.status,
        statusText: response.statusText,
        contentType: response.headers.get('Content-Type'),
      });

      if (!response.ok) {
        let errorMessage = `Server returned ${response.status}`;
        try {
          const errorText = await response.text();
          errorMessage += `: ${errorText}`;
        } catch (e) {
          errorMessage += ' (no error details available)';
        }
        throw new Error(errorMessage);
      }

      // Verify we got a PDF back
      const contentType = response.headers.get('Content-Type');
      if (!contentType?.includes('application/pdf')) {
        throw new Error(`Expected PDF but got ${contentType}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'research-report.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error) {
      console.error('PDF download failed:', error);
      alert(`Failed to generate PDF: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  return (
    <Paper className="mt-8 p-6">
      <Typography variant="h5" component="h2" className="mb-4">
        Research Report
      </Typography>

      <Typography component="div" className="whitespace-pre-wrap mb-6">
        {report}
      </Typography>

      <Button 
        variant="contained" 
        onClick={handleDownloadPDF}
        className="mb-6"
      >
        Download PDF
      </Button>

      <Typography variant="h6" component="h3" className="mb-2">
        Sources
      </Typography>
      
      <List>
        {sources.map((source, index) => (
          <ListItem key={index}>
            <Link href={source} target="_blank" rel="noopener noreferrer">
              {source}
            </Link>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
} 