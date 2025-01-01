import { useState } from 'react';
import { TextField, Button, Box, Alert } from '@mui/material';
import axios from 'axios';

interface ResearchFormProps {
  onReport: (data: { report: string; sources: string[] }) => void;
  setLoading: (loading: boolean) => void;
}

export default function ResearchForm({ onReport, setLoading }: ResearchFormProps) {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      window.sessionStorage.setItem('lastQuery', query);
      
      const response = await axios.post('/api/research', {
        query: query
      });
      
      if (response.data && response.data.report) {
        onReport({
          report: response.data.report,
          sources: response.data.sources || []
        });
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Research error:', err);
      setError('Failed to generate research report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} className="space-y-4">
      <TextField
        fullWidth
        label="Enter your research topic"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        required
      />
      
      <Button 
        type="submit" 
        variant="contained" 
        fullWidth
        disabled={!query}
      >
        Generate Report
      </Button>

      {error && (
        <Alert severity="error" className="mt-4">
          {error}
        </Alert>
      )}
    </Box>
  );
} 