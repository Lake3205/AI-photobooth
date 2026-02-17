import { Chart } from 'chart.js';
import type { ChartConfiguration } from 'chart.js';

// Predefined colors for each model to ensure consistency
const modelColors: Record<string, { solid: string; transparent: string }> = {
  gemini: {
    solid: 'rgb(66, 133, 244)',
    transparent: 'rgba(66, 133, 244, 0.2)'
  },
  claude: {
    solid: 'rgb(204, 143, 102)',
    transparent: 'rgba(204, 143, 102, 0.2)'
  },
  openai: {
    solid: 'rgb(116, 195, 151)',
    transparent: 'rgba(116, 195, 151, 0.2)'
  }
};

function getModelColor(model: string) {
  return modelColors[model] || {
    solid: `rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`,
    transparent: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.2)`
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
    bins.push({ start, end, count: 0 });
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

// Create a combined histogram for percentage data (0-100 range)
function createCombinedPercentageChart(
  canvas: HTMLCanvasElement,
  label: string,
  modelValues: Record<string, number[]>
) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  const datasets = Object.entries(modelValues).map(([model, values]) => {
    const bins = createBins(values, 0, 100, 50);
    const colors = getModelColor(model);

    return {
      label: `${model.charAt(0).toUpperCase() + model.slice(1)} (Avg: ${calculateAverage(values).toFixed(1)}%)`,
      data: bins.map(bin => bin.count),
      borderColor: colors.solid,
      backgroundColor: colors.transparent,
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointRadius: 0,
      pointHoverRadius: 4
    };
  });

  // Use the bins from the first model for labels (they're all the same range)
  const firstValues = Object.values(modelValues)[0];
  const bins = createBins(firstValues || [], 0, 100, 50);

  const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: bins.map(bin => `${bin.start}-${bin.end}%`),
      datasets
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

// Create a combined histogram for years/hours data (0-120 range)
function createCombinedYearsChart(
  canvas: HTMLCanvasElement,
  label: string,
  modelValues: Record<string, number[]>
) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  const datasets = Object.entries(modelValues).map(([model, values]) => {
    const bins = createBins(values, 0, 120, 60);
    const colors = getModelColor(model);

    return {
      label: `${model.charAt(0).toUpperCase() + model.slice(1)} (Avg: ${calculateAverage(values).toFixed(1)})`,
      data: bins.map(bin => bin.count),
      borderColor: colors.solid,
      backgroundColor: colors.transparent,
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointRadius: 0,
      pointHoverRadius: 4
    };
  });

  const firstValues = Object.values(modelValues)[0];
  const bins = createBins(firstValues || [], 0, 120, 60);

  const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: bins.map(bin => `${bin.start}-${bin.end}`),
      datasets
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

// Create a combined histogram for numeric data
function createCombinedNumericChart(
  canvas: HTMLCanvasElement,
  label: string,
  modelValues: Record<string, number[]>,
  format: string
) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  // Find global min and max across all models
  const allValues = Object.values(modelValues).flat();
  const min = Math.min(...allValues);
  const max = Math.max(...allValues);

  const formatValue = (val: number) => {
    if (format === 'currency') return `€${val.toFixed(2)}`;
    if (format === 'weight') return `${Math.round(val)}kg`;
    return val.toString();
  };

  const datasets = Object.entries(modelValues).map(([model, values]) => {
    const bins = createBins(values, min, max, 50);
    const colors = getModelColor(model);
    const avg = calculateAverage(values);

    return {
      label: `${model.charAt(0).toUpperCase() + model.slice(1)} (Avg: ${formatValue(avg)})`,
      data: bins.map(bin => bin.count),
      borderColor: colors.solid,
      backgroundColor: colors.transparent,
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointRadius: 0,
      pointHoverRadius: 4
    };
  });

  const bins = createBins(allValues, min, max, 50);

  const config: ChartConfiguration = {
    type: 'line',
    data: {
      labels: bins.map(bin => `${formatValue(bin.start)}-${formatValue(bin.end)}`),
      datasets
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
            label: (context) => `${context.dataset.label}: ${context.parsed.y} people`
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

// Create a combined pie/bar chart for text data
function createCombinedTextChart(
  canvas: HTMLCanvasElement,
  label: string,
  modelValues: Record<string, string[]>
) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;

  // Get all unique values across all models
  const allUniqueValues = new Set<string>();
  Object.values(modelValues).forEach(values => {
    values.forEach(v => allUniqueValues.add(v));
  });
  const labels = Array.from(allUniqueValues).sort();

  // Create a dataset for each model
  const datasets = Object.entries(modelValues).map(([model, values]) => {
    const counts: Record<string, number> = {};
    labels.forEach(label => counts[label] = 0);
    
    values.forEach(value => {
      counts[value] = (counts[value] || 0) + 1;
    });

    const colors = getModelColor(model);

    return {
      label: `${model.charAt(0).toUpperCase() + model.slice(1)} (${values.length} total)`,
      data: labels.map(l => counts[l] ?? 0) as number[],
      backgroundColor: colors.transparent,
      borderColor: colors.solid,
      borderWidth: 2
    };
  });

  const config: ChartConfiguration = {
    type: 'bar',
    data: {
      labels,
      datasets
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
            label: (context) => {
              const value = context.parsed.y;
              if (value === null || value === undefined) return '';
              const dataset = context.dataset as any;
              const total = (dataset.data as number[]).reduce((sum: number, val: number) => sum + val, 0);
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0';
              return `${context.dataset.label}: ${value} (${percentage}%)`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Count'
          }
        },
        x: {
          title: {
            display: true,
            text: label
          }
        }
      }
    }
  };

  return new Chart(ctx, config);
}

export function createCombinedChartForAssumption(
  canvas: HTMLCanvasElement,
  assumption: { 
    name: string; 
    format: string; 
    modelValues: Record<string, (string | number)[]> 
  }
): Chart | null {
  if (Object.keys(assumption.modelValues).length === 0) return null;

  switch (assumption.format) {
    case 'percentage':
      return createCombinedPercentageChart(
        canvas, 
        assumption.name, 
        assumption.modelValues as Record<string, number[]>
      );

    case 'years':
    case 'hours_per_day':
      return createCombinedYearsChart(
        canvas, 
        assumption.name, 
        assumption.modelValues as Record<string, number[]>
      );

    case 'currency':
    case 'number':
    case 'weight':
      return createCombinedNumericChart(
        canvas, 
        assumption.name, 
        assumption.modelValues as Record<string, number[]>, 
        assumption.format
      );

    case 'text':
      return createCombinedTextChart(
        canvas, 
        assumption.name, 
        assumption.modelValues as Record<string, string[]>
      );

    default:
      console.warn(`Unknown format type: ${assumption.format}`);
      return null;
  }
}
