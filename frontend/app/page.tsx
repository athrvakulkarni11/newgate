'use client';

import { useState } from 'react';
import ResearchForm from '../components/ResearchForm';
import ResearchReport from '../components/ResearchReport';
import { Container, Typography } from '@mui/material';

export default function Home() {
  const [report, setReport] = useState<string>('');
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  return (
    <Container maxWidth="lg" className="py-8">
      <Typography variant="h3" component="h1" className="mb-8 text-center">
        Research Assistant
      </Typography>
      
      <ResearchForm 
        onReport={(data) => {
          setReport(data.report);
          setSources(data.sources);
        }}
        setLoading={setLoading}
      />
      
      {report && <ResearchReport report={report} sources={sources} />}
    </Container>
  );
} 