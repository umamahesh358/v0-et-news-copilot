'use client';

import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertCircle, Loader2, Search, MessageSquare, TrendingUp, AlertTriangle } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Mock data for when backend is unavailable
const mockBriefings: Record<string, any> = {
  investor: {
    briefing: {
      what_happened: "RBI announces new AI regulation framework for financial institutions, requiring companies to implement safeguards by June 2025.",
      why_it_matters: "As an investor, this impacts fintech valuations, potential compliance costs, and competitive advantages for companies with strong AI governance.",
      who_involved: "Reserve Bank of India (RBI), NASSCOM, major fintech companies (PhonePe, Paytm, CRED), regulatory bodies",
      what_next: "Industry consultation phase starts in April 2025, with expected guidance document release by May 2025"
    },
    related_articles: [
      {
        title: "Fintech Companies React to RBI AI Rules",
        snippet: "Industry leaders discuss compliance strategies and potential business impact...",
        similarity_score: 0.96,
        date: "2025-03-24"
      },
      {
        title: "Global AI Regulation Trends Affecting India",
        snippet: "How international regulatory frameworks influence Indian fintech policy...",
        similarity_score: 0.92,
        date: "2025-03-20"
      },
      {
        title: "AI Risk Management in Banking Sector",
        snippet: "Best practices for managing algorithmic risks in financial services...",
        similarity_score: 0.88,
        date: "2025-03-18"
      }
    ]
  },
  student: {
    briefing: {
      what_happened: "Government introduces AI regulation guidelines that banks and fintech companies must follow starting mid-2025.",
      why_it_matters: "Understanding AI regulation helps you learn how governments balance innovation with consumer protection, important career knowledge.",
      who_involved: "Government regulatory bodies, banks, tech companies, consumer protection advocates",
      what_next: "Companies will start implementing AI compliance programs, creating job opportunities in compliance and AI ethics"
    },
    related_articles: [
      {
        title: "AI Ethics and Regulation Fundamentals",
        snippet: "A comprehensive overview of why AI regulation matters...",
        similarity_score: 0.94,
        date: "2025-03-22"
      },
      {
        title: "Career Opportunities in AI Compliance",
        snippet: "New jobs emerging in the AI governance and compliance space...",
        similarity_score: 0.90,
        date: "2025-03-19"
      }
    ]
  },
  founder: {
    briefing: {
      what_happened: "RBI mandates AI governance requirements for all financial service providers, with compliance deadline of June 2025.",
      why_it_matters: "Your startup needs to implement AI compliance framework immediately. This affects product roadmap, hiring, and potentially raises funding timelines.",
      who_involved: "Your competitors, regulators, enterprise customers evaluating vendors based on compliance status",
      what_next: "Start building compliance framework now. Consider hiring a compliance officer and conducting AI risk audit before June 2025"
    },
    related_articles: [
      {
        title: "Startup Compliance Strategy for AI Regulation",
        snippet: "How to build compliance without slowing innovation...",
        similarity_score: 0.97,
        date: "2025-03-23"
      },
      {
        title: "Fundraising During Regulatory Changes",
        snippet: "How regulation affects Series A/B rounds in fintech...",
        similarity_score: 0.91,
        date: "2025-03-21"
      }
    ]
  },
  journalist: {
    briefing: {
      what_happened: "RBI releases first-ever comprehensive AI regulation framework for financial sector after months of consultation.",
      why_it_matters: "This is a landmark moment in India's tech policy, affecting millions of users of fintech services and representing shift toward proactive regulation.",
      who_involved: "Government agencies, RBI, tech companies, consumer groups, industry associations",
      what_next: "Story updates expected in April with company responses and implementation plans"
    },
    related_articles: [
      {
        title: "Timeline: Evolution of AI Regulation in India",
        snippet: "How regulatory approach has changed over the past 3 years...",
        similarity_score: 0.95,
        date: "2025-03-20"
      }
    ]
  }
};

const mockQAAnswers: Record<string, any> = {
  investor: {
    answer: "Based on the regulation, startup valuations in the fintech space may face downward pressure in Q2 2025 during compliance implementation phase. However, companies with strong AI governance may see premium valuations as institutional investors prefer safer investments. Mid-to-long term, regulation creates barriers to entry that favor well-capitalized companies.",
    citations: [
      {
        source: "RBI AI Regulation Framework",
        excerpt: "All AI systems must be audited and validated before deployment in customer-facing applications",
        relevance_score: 0.98
      },
      {
        source: "Fintech Investment Analysis Report",
        excerpt: "Compliance costs average 2-5% of revenue for mid-sized fintech companies during first year",
        relevance_score: 0.92
      }
    ]
  },
  default: {
    answer: "Based on the information provided, the regulation will require all companies to implement AI governance frameworks before June 2025. This includes risk assessment, bias testing, and transparent disclosure of AI usage to customers. Companies that proactively implement these measures may gain competitive advantage.",
    citations: [
      {
        source: "Source Article",
        excerpt: "Regulation requires transparency and accountability in AI decision-making systems",
        relevance_score: 0.95
      }
    ]
  }
};

export default function Page() {
  const [articleUrl, setArticleUrl] = useState('');
  const [articleText, setArticleText] = useState('');
  const [persona, setPersona] = useState('investor');
  const [loading, setLoading] = useState(false);
  const [briefing, setBriefing] = useState<any>(null);
  const [relatedArticles, setRelatedArticles] = useState<any[]>([]);
  const [qaQuestion, setQaQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState<any>(null);
  const [dbStats, setDbStats] = useState<any>(null);
  const [error, setError] = useState('');
  const [backendAvailable, setBackendAvailable] = useState(false);
  const [useMockData, setUseMockData] = useState(true);

  // Check if backend is available on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch(`${API_URL}/health`, { timeout: 3000 });
        if (response.ok) {
          setBackendAvailable(true);
          setUseMockData(false);
          fetchDbStats();
        }
      } catch (err) {
        // Backend not available, use mock data
        setBackendAvailable(false);
        setUseMockData(true);
      }
    };

    checkBackend();
  }, []);

  // Fetch database stats on mount
  const fetchDbStats = async () => {
    try {
      const response = await fetch(`${API_URL}/api/db-stats`);
      if (response.ok) {
        const data = await response.json();
        setDbStats(data);
      }
    } catch (err) {
      console.error('Failed to fetch DB stats:', err);
    }
  };

  const handleGenerateBriefing = async () => {
    if (!articleText.trim()) {
      setError('Please enter article text');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      // Use mock data if backend is unavailable
      if (useMockData) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const mockData = mockBriefings[persona] || mockBriefings.investor;
        setBriefing(mockData.briefing);
        setRelatedArticles(mockData.related_articles);
        return;
      }

      // Call real API if backend is available
      const response = await fetch(`${API_URL}/api/briefing`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          article_text: articleText,
          article_url: articleUrl || null,
          persona,
        }),
      });

      if (!response.ok) throw new Error('Failed to generate briefing');
      const data = await response.json();
      setBriefing(data.briefing);
      setRelatedArticles(data.related_articles || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!qaQuestion.trim() || !articleText.trim()) {
      setError('Please enter a question and article text');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      // Use mock data if backend is unavailable
      if (useMockData) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        const mockAnswer = mockQAAnswers[persona] || mockQAAnswers.default;
        setQaAnswer(mockAnswer);
        return;
      }

      // Call real API if backend is available
      const response = await fetch(`${API_URL}/api/ask-question`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: qaQuestion,
          article_text: articleText,
          use_related: true,
          persona,
        }),
      });

      if (!response.ok) throw new Error('Failed to answer question');
      const data = await response.json();
      setQaAnswer(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Status Banner */}
      {useMockData && (
        <div className="bg-amber-50 border-b border-amber-200">
          <div className="max-w-6xl mx-auto px-4 py-3">
            <div className="flex items-center gap-3">
              <AlertTriangle className="h-5 w-5 text-amber-600 flex-shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-medium text-amber-900">
                  Using sample data for demonstration. 
                  <span className="ml-2 text-amber-700">
                    Backend not connected - using realistic mock responses.
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="border-b bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">ET News Copilot</h1>
              <p className="text-slate-600 mt-1">Transform articles into intelligent briefings</p>
            </div>
            <div className="text-right text-sm">
              {backendAvailable && dbStats && (
                <div className="text-slate-600">
                  <div className="text-green-600 font-medium">✓ Backend Connected</div>
                  <div className="text-xs text-slate-500">{dbStats.total_articles || 0} articles in DB</div>
                </div>
              )}
              {useMockData && (
                <div className="text-amber-600">
                  <div className="font-medium">Demo Mode</div>
                  <div className="text-xs text-amber-500">Sample data</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-4 py-8">
        {error && (
          <Card className="mb-6 p-4 border-red-200 bg-red-50">
            <div className="flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-medium text-red-900">Error</p>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </Card>
        )}

        {/* Article Input */}
        <Card className="p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Paste Your Article</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Article URL (optional)</label>
              <Input
                placeholder="https://example.com/article"
                value={articleUrl}
                onChange={(e) => setArticleUrl(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Article Text</label>
              <textarea
                className="w-full h-32 p-3 border rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Paste your article content here..."
                value={articleText}
                onChange={(e) => setArticleText(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Select Persona</label>
              <div className="flex gap-2">
                {['investor', 'student', 'founder', 'journalist'].map((p) => (
                  <button
                    key={p}
                    onClick={() => setPersona(p)}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                      persona === p
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-200 text-slate-700 hover:bg-slate-300'
                    }`}
                  >
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <Button
              onClick={handleGenerateBriefing}
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                'Generate Briefing'
              )}
            </Button>
          </div>
        </Card>

        {/* Results */}
        {briefing && (
          <Tabs defaultValue="briefing" className="space-y-4">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="briefing">Briefing</TabsTrigger>
              <TabsTrigger value="related">Related ({relatedArticles.length})</TabsTrigger>
              <TabsTrigger value="qa">Q&A</TabsTrigger>
            </TabsList>

            <TabsContent value="briefing" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { icon: '💡', title: 'What Happened', content: briefing.what_happened },
                  { icon: '💰', title: 'Why It Matters', content: briefing.why_it_matters },
                  { icon: '👥', title: 'Who&apos;s Involved', content: briefing.who_involved },
                  { icon: '🔮', title: 'What Next', content: briefing.what_next },
                ].map((item) => (
                  <Card key={item.title} className="p-4">
                    <div className="flex items-start gap-3">
                      <span className="text-2xl">{item.icon}</span>
                      <div className="flex-1">
                        <h3 className="font-semibold mb-2">{item.title}</h3>
                        <p className="text-sm text-slate-700">{item.content}</p>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="related" className="space-y-4">
              {relatedArticles.length === 0 ? (
                <Card className="p-8 text-center text-slate-500">
                  <Search className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>No related articles found</p>
                </Card>
              ) : (
                <div className="space-y-3">
                  {relatedArticles.map((article, i) => (
                    <Card key={i} className="p-4 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start gap-4">
                        <div>
                          <h4 className="font-medium">{article.title}</h4>
                          <p className="text-sm text-slate-600 mt-1">{article.snippet}</p>
                        </div>
                        <div className="text-right text-sm">
                          <div className="font-medium text-blue-600">
                            {Math.round(article.similarity_score * 100)}%
                          </div>
                          <div className="text-xs text-slate-500">{article.date}</div>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              )}
            </TabsContent>

            <TabsContent value="qa" className="space-y-4">
              <Card className="p-4">
                <label className="block text-sm font-medium mb-2">Ask a Question</label>
                <div className="flex gap-2">
                  <Input
                    placeholder="e.g., How will this affect my business?"
                    value={qaQuestion}
                    onChange={(e) => setQaQuestion(e.target.value)}
                  />
                  <Button
                    onClick={handleAskQuestion}
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <MessageSquare className="h-4 w-4" />}
                  </Button>
                </div>
              </Card>

              {qaAnswer && (
                <div className="space-y-4">
                  <Card className="p-4 bg-blue-50 border-blue-200">
                    <p className="text-sm font-medium text-blue-900 mb-2">Answer</p>
                    <p className="text-slate-700">{qaAnswer.answer}</p>
                  </Card>

                  {qaAnswer.citations && qaAnswer.citations.length > 0 && (
                    <Card className="p-4">
                      <p className="text-sm font-medium mb-3 flex items-center gap-2">
                        <TrendingUp className="h-4 w-4" />
                        Sources
                      </p>
                      <div className="space-y-2">
                        {qaAnswer.citations.map((citation: any, i: number) => (
                          <div key={i} className="text-sm p-2 bg-slate-50 rounded border border-slate-200">
                            <p className="font-medium text-slate-900">{citation.source}</p>
                            <p className="text-slate-600 text-xs mt-1">"{citation.excerpt}"</p>
                            <p className="text-slate-500 text-xs mt-1">Relevance: {Math.round(citation.relevance_score * 100)}%</p>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}
                </div>
              )}
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  );
}
