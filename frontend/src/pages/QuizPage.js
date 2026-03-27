import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { quizAPI } from '../api';
import { CheckCircle, Circle, ArrowRight, ArrowLeft, Clock } from 'lucide-react';
import { toast } from 'sonner';

const QuizPage = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [timeLeft, setTimeLeft] = useState(15 * 60); // 15 minutes in seconds
  const questionsPerPage = 5;

  // This should ideally come from your user context/profile
  // For now, it defaults to 'male' to test the filtering
  const userGender = 'male'; 

  useEffect(() => {
    loadQuestions();
  }, []);

  // Timer Logic
  useEffect(() => {
    if (timeLeft <= 0) {
      handleAutoSubmit();
      return;
    }
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft]);

  const loadQuestions = async () => {
    try {
      const response = await quizAPI.getQuestions();
      setQuestions(response.data.questions);
    } catch (error) {
      toast.error('Failed to load questions');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const handleAutoSubmit = () => {
    toast.error("Time's up! Submitting your current answers.");
    handleSubmit();
  };

  // --- GENDER FILTERING LOGIC ---
  const filteredQuestions = questions.filter(q => {
    // If question is gender-specific, check if it matches userGender
    if (q.gender_target === 'female' && userGender === 'male') return false;
    if (q.gender_target === 'male' && userGender === 'female') return false;
    return true;
  });

  const totalPages = Math.ceil(filteredQuestions.length / questionsPerPage);
  
  const currentQuestions = filteredQuestions.slice(
    currentPage * questionsPerPage,
    (currentPage + 1) * questionsPerPage
  );

  // Progress is now calculated based on the filtered list
  const progress = filteredQuestions.length > 0 
    ? ((Object.keys(answers).length / filteredQuestions.length) * 100).toFixed(0) 
    : 0;

  const handleAnswer = (questionId, value) => {
    setAnswers({
      ...answers,
      [questionId]: value,
    });
  };

  const handleSubmit = async () => {
    // Check all applicable questions are answered
    if (timeLeft > 0 && Object.keys(answers).length < filteredQuestions.length) {
      toast.error('Please answer all applicable questions');
      return;
    }

    setLoading(true);
    try {
      // Pass gender to backend so scoring is accurate
      const response = await quizAPI.submitQuiz({ 
        answers, 
        gender: userGender 
      });
      toast.success('Assessment completed!');
      navigate('/dashboard/results', { state: { results: response.data } });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit quiz');
    } finally {
      setLoading(false);
    }
  };

  const canGoNext = currentPage < totalPages - 1;
  const canGoPrev = currentPage > 0;
  const isLastPage = currentPage === totalPages - 1;

  return (
    <div className="p-6 md:p-12" data-testid="quiz-page">
      <div className="max-w-3xl mx-auto">
        {/* Header with Timer */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Health Assessment Quiz</h1>
            <p className="text-slate-600">Answer honestly for an accurate assessment.</p>
          </div>
          <div className={`flex items-center space-x-2 px-4 py-2 rounded-full border-2 ${timeLeft < 60 ? 'border-red-500 text-red-500 animate-pulse' : 'border-sage-teal text-sage-teal'}`}>
            <Clock className="w-5 h-5" />
            <span className="font-mono text-xl font-bold">{formatTime(timeLeft)}</span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-slate-600">
              Question {currentPage * questionsPerPage + 1}-
              {Math.min((currentPage + 1) * questionsPerPage, filteredQuestions.length)} of {filteredQuestions.length}
            </span>
            <span className="text-sm font-medium text-sage-teal">{progress}% Complete</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-2">
            <div
              className="bg-sage-teal h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Questions */}
        <div className="space-y-6 mb-8">
          {currentQuestions.map((question) => {
            const answer = answers[question.id];

            return (
              <div key={question.id} className="card-dashboard p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-xs font-semibold uppercase tracking-wider text-sage-teal bg-sage-teal/10 px-2 py-1 rounded">
                        {question.category}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-slate-800 leading-relaxed">
                      {question.question}
                    </h3>
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    onClick={() => handleAnswer(question.id, true)}
                    className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-lg border-2 transition-all ${
                      answer === true
                        ? 'border-sage-teal bg-sage-teal text-white'
                        : 'border-slate-200 hover:border-sage-teal text-slate-600'
                    }`}
                  >
                    <span className="font-medium">Yes</span>
                  </button>

                  <button
                    onClick={() => handleAnswer(question.id, false)}
                    className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-lg border-2 transition-all ${
                      answer === false
                        ? 'border-sage-teal bg-sage-teal text-white'
                        : 'border-slate-200 hover:border-sage-teal text-slate-600'
                    }`}
                  >
                    <span className="font-medium">No</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center">
          <button
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={!canGoPrev}
            className="flex items-center space-x-2 px-6 py-3 rounded-lg border-2 border-slate-200 text-slate-600 hover:border-sage-teal disabled:opacity-50 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Previous</span>
          </button>

          {isLastPage ? (
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="bg-sage-teal text-white px-8 py-3 rounded-lg font-bold hover:bg-opacity-90 transition-all disabled:opacity-50"
            >
              {loading ? 'Submitting...' : 'Submit Assessment'}
            </button>
          ) : (
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={!canGoNext}
              className="flex items-center space-x-2 bg-sage-teal text-white px-8 py-3 rounded-lg font-bold hover:bg-opacity-90"
            >
              <span>Next</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default QuizPage;