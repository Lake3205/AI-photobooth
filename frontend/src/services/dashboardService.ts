import { Chart, registerables } from 'chart.js';
import type { ChartConfiguration } from 'chart.js';
import { authService } from './authService';
import type { FormQuestions, questionType } from '@/types/FormTypes';

Chart.register(...registerables);

export interface AssumptionValue {
    name: string;
    format: string;
    value: string | number;
}

export interface AssumptionRecord {
    id: number;
    ai_model: string;
    assumptions: Record<string, AssumptionValue>;
    date_created: string;
}

export interface DashboardQuestion {
    key: string;
    id: number;
    question: string;
    type: questionType;
    scale?: [number, number];
}

export interface FormResult {
    id: number;
    question: string;
    type: questionType;
    scale?: [number, number];
    answers: Array<{
        value: string;
        explanation?: string;
    }>;
}

function parseQuestionId(questionKey: string): number {
    const parsed = Number.parseInt(questionKey.replace('q_', ''), 10);
    return Number.isNaN(parsed) ? -1 : parsed;
}

export async function fetchFormQuestions(): Promise<DashboardQuestion[]> {
    const response = await authService.authenticatedFetch(`${import.meta.env.VITE_API_URL}/form/questions`);
    if (!response.ok) {
        throw new Error('Failed to fetch form questions');
    }

    const questions = (await response.json()) as FormQuestions;

    return Object.entries(questions)
        .map(([key, value]) => ({
            key,
            id: parseQuestionId(key),
            question: value.question,
            type: value.type,
            scale: value.scale,
        }))
        .filter((question) => question.id > 0)
        .sort((a, b) => a.id - b.id);
}

export async function addFormQuestion(payload: { question: string; type: questionType; scale?: [number, number] }): Promise<void> {
    const response = await authService.authenticatedFetch(`${import.meta.env.VITE_API_URL}/form/questions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        throw new Error('Failed to add question');
    }
}

export async function removeFormQuestion(questionId: number): Promise<void> {
    const response = await authService.authenticatedFetch(`${import.meta.env.VITE_API_URL}/form/questions/${questionId}`, {
        method: 'DELETE',
    });

    if (!response.ok) {
        throw new Error('Failed to delete question');
    }
}

// Get data fom backend API
export async function fetchAssumptions(aiModel: string): Promise<AssumptionRecord[]> {
    try {
        // Use authenticated fetch to get data
        const response = await authService.authenticatedFetch(
            `${import.meta.env.VITE_API_URL}/database/assumptions/${aiModel}`
        );
        if (!response.ok) {
            throw new Error(`Failed to fetch assumptions: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching assumptions:', error);
        throw error;
    }
}

// Group assumptions by format type
export function groupAssumptionsByFormat(records: AssumptionRecord[]) {
    const grouped: Record<string, { name: string; format: string; values: (string | number)[] }> = {};

    records.forEach(record => {
        Object.entries(record.assumptions).forEach(([key, assumption]) => {
            if (!grouped[key]) {
                grouped[key] = {
                    name: assumption.name,
                    format: assumption.format,
                    values: []
                };
            }
            if (assumption.value !== null && assumption.value !== undefined) {
                grouped[key].values.push(assumption.value);
            }
        });
    });

    return grouped;
}

function getRandomColor() {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return {
        solid: `rgb(${r}, ${g}, ${b})`,
        transparent: `rgba(${r}, ${g}, ${b}, 0.2)`
    };
}

function calculateAverage(values: number[]): number {
    if (values.length === 0) return 0;
    const sum = values.reduce((acc, val) => acc + val, 0);
    return sum / values.length;
}

function createBins(values: number[], min: number, max: number, binCount: number) {
    const binSize = (max - min) / binCount;
    const bins: { start: number; end: number; count: number }[] = [];

    for (let i = 0; i < binCount; i++) {
        const start = Math.round(min + i * binSize);
        const end = Math.round(min + (i + 1) * binSize);
        bins.push({start, end, count: 0});
    }

    values.forEach(value => {
        const binIndex = Math.min(
            Math.floor((value - min) / binSize),
            binCount - 1
        );
        if (binIndex >= 0 && binIndex < bins.length) {
            const bin = bins[binIndex];
            if (bin) {
                bin.count++;
            }
        }
    });

    return bins;
}

// Create a histogram for percentage data (0-100 range)
export function createPercentageChart(canvas: HTMLCanvasElement, label: string, values: number[]) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    // Create bins for the histogram
    const bins = createBins(values, 0, 100, 50);
    const colors = getRandomColor();

    const config: ChartConfiguration = {
        type: 'line',
        data: {
            labels: bins.map(bin => `${bin.start}-${bin.end}%`),
            datasets: [{
                label: `Count (Avg: ${calculateAverage(values).toFixed(1)}%)`,
                data: bins.map(bin => bin.count),
                borderColor: colors.solid,
                backgroundColor: colors.transparent,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: `${label} Distribution`
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of People'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: label
                    },
                    ticks: {
                        maxTicksLimit: 30,
                        autoSkip: true
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// Create a histogram for years/hours data (0-120 range)
export function createYearsChart(canvas: HTMLCanvasElement, label: string, values: number[]) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    // Create bins for the histogram
    const bins = createBins(values, 0, 120, 60);
    const colors = getRandomColor();

    const config: ChartConfiguration = {
        type: 'line',
        data: {
            labels: bins.map(bin => `${bin.start}-${bin.end}`),
            datasets: [{
                label: `Count (Avg: ${calculateAverage(values).toFixed(1)})`,
                data: bins.map(bin => bin.count),
                borderColor: colors.solid,
                backgroundColor: colors.transparent,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: `${label} Distribution`
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of People'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: label
                    },
                    ticks: {
                        maxTicksLimit: 30,
                        autoSkip: true
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// Create a histogram for numeric data (int, number, weight)
export function createNumericChart(canvas: HTMLCanvasElement, label: string, values: number[], format: string) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    const avg = calculateAverage(values);
    const min = Math.min(...values);
    const max = Math.max(...values);

    const formatValue = (val: number) => {
        if (format === 'currency') return `€${val.toFixed(2)}`;
        if (format === 'weight') return `${Math.round(val)}kg`;
        return val.toString();
    };

    // Create bins for the histogram
    const bins = createBins(values, min, max, 50);
    const colors = getRandomColor();

    const config: ChartConfiguration = {
        type: 'line',
        data: {
            labels: bins.map(bin => `${formatValue(bin.start)}-${formatValue(bin.end)}`),
            datasets: [{
                label: `Count (Avg: ${formatValue(avg)})`,
                data: bins.map(bin => bin.count),
                borderColor: colors.solid,
                backgroundColor: colors.transparent,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: `${label} Distribution`
                },
                tooltip: {
                    callbacks: {
                        label: (context) => `People: ${context.parsed.y}`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of People'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: label
                    },
                    ticks: {
                        maxTicksLimit: 30,
                        autoSkip: true
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// Create a pie chart for text data
export function createTextChart(canvas: HTMLCanvasElement, label: string, values: string[]) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    const counts: Record<string, number> = {};
    values.forEach(value => {
        counts[value] = (counts[value] || 0) + 1;
    });

    const labels = Object.keys(counts);
    const data = Object.values(counts);
    const total = data.reduce((sum, val) => sum + val, 0);

    // Generate random colors for each slice
    const colors = labels.map(() => {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return `rgba(${r}, ${g}, ${b}, 0.8)`;
    });

    const config: ChartConfiguration = {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.8', '1')),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'right'
                },
                title: {
                    display: true,
                    text: `${label} Distribution (${total} entries)`
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const value = context.parsed;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

export function createChartForAssumption(
    canvas: HTMLCanvasElement,
    assumption: { name: string; format: string; values: (string | number)[] }
): Chart | null {
    if (assumption.values.length === 0) return null;

    switch (assumption.format) {
        case 'percentage':
            return createPercentageChart(canvas, assumption.name, assumption.values as number[]);

        case 'years':
        case 'hours_per_day':
            return createYearsChart(canvas, assumption.name, assumption.values as number[]);

        case 'currency':
        case 'number':
        case 'weight':
            return createNumericChart(canvas, assumption.name, assumption.values as number[], assumption.format);

        case 'text':
            return createTextChart(canvas, assumption.name, assumption.values as string[]);

        default:
            console.warn(`Unknown format type: ${assumption.format}`);
            return null;
    }
}

// Fetch form results for analytics
export async function fetchFormResults(): Promise<FormResult[]> {
    const response = await authService.authenticatedFetch(`${import.meta.env.VITE_API_URL}/form/results`);
    if (!response.ok) {
        throw new Error('Failed to fetch form results');
    }
    return await response.json();
}

// Create a bar or line chart for scale questions (depending on range)
export function createScaleChart(canvas: HTMLCanvasElement, question: FormResult): Chart | null {
    const ctx = canvas.getContext('2d');
    if (!ctx || !question.scale) return null;

    const [min, max] = question.scale;
    const range = max - min + 1;
    const values = question.answers
        .map(a => parseInt(a.value))
        .filter(v => !isNaN(v));

    if (values.length === 0) return null;

    // Count occurrences of each value
    const counts: Record<number, number> = {};
    for (let i = min; i <= max; i++) {
        counts[i] = 0;
    }
    values.forEach(v => {
        if (v >= min && v <= max) {
            counts[v] = (counts[v] || 0) + 1;
        }
    });

    const labels = Object.keys(counts).map(k => k.toString());
    const data = Object.values(counts);
    const colors = getRandomColor();

    const avg = calculateAverage(values);

    // Use line chart if range > 20, otherwise bar chart
    const chartType = range > 20 ? 'line' : 'bar';
    
    const datasetConfig: any = {
        label: `Responses (Avg: ${avg.toFixed(1)})`,
        data: data,
        backgroundColor: colors.transparent,
        borderColor: colors.solid,
        borderWidth: 2
    };

    // Add line-specific styling
    if (chartType === 'line') {
        datasetConfig.fill = true;
        datasetConfig.tension = 0.4;
        datasetConfig.pointRadius = 3;
        datasetConfig.pointHoverRadius = 6;
    }

    const config: ChartConfiguration = {
        type: chartType,
        data: {
            labels: labels,
            datasets: [datasetConfig]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: question.question
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    },
                    title: {
                        display: true,
                        text: 'Number of Responses'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Rating'
                    },
                    ticks: {
                        maxTicksLimit: 30,
                        autoSkip: true
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// Create a pie chart for yes/no questions
export function createYesNoChart(canvas: HTMLCanvasElement, question: FormResult): Chart | null {
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    const values = question.answers.map(a => a.value.toLowerCase());
    if (values.length === 0) return null;

    const yesCounts = values.filter(v => v === 'yes').length;
    const noCounts = values.filter(v => v === 'no').length;
    const total = yesCounts + noCounts;

    if (total === 0) return null;

    const config: ChartConfiguration = {
        type: 'pie',
        data: {
            labels: ['Yes', 'No'],
            datasets: [{
                label: 'Responses',
                data: [yesCounts, noCounts],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',   // green for yes
                    'rgba(239, 68, 68, 0.8)'     // red for no
                ],
                borderColor: [
                    'rgba(34, 197, 94, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'right'
                },
                title: {
                    display: true,
                    text: question.question
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const value = context.parsed;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

export function createChartForFormQuestion(canvas: HTMLCanvasElement, question: FormResult): Chart | null {
    if (question.answers.length === 0) return null;

    switch (question.type) {
        case 'scale':
            return createScaleChart(canvas, question);

        case 'yes_no_explain':
            return createYesNoChart(canvas, question);

        default:
            console.warn(`Unknown question type: ${question.type}`);
            return null;
    }
}
