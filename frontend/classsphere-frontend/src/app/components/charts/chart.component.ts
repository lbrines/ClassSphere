import { Component, OnInit, Input, signal, computed, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string | string[];
  borderWidth?: number;
  fill?: boolean;
}

interface ChartOptions {
  responsive: boolean;
  maintainAspectRatio: boolean;
  plugins?: {
    legend?: {
      display: boolean;
      position?: string;
    };
    title?: {
      display: boolean;
      text: string;
    };
  };
  scales?: {
    y?: {
      beginAtZero: boolean;
    };
    x?: {
      beginAtZero: boolean;
    };
  };
}

@Component({
  selector: 'app-chart',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <!-- Chart Header -->
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ chartTitle() }}
          </h3>
          <div class="flex space-x-2">
            <button
              (click)="toggleChartType()"
              class="text-sm text-indigo-600 hover:text-indigo-500"
            >
              {{ getChartTypeLabel() }}
            </button>
            @if (showDrillDown) {
              <button
                (click)="resetDrillDown()"
                class="text-sm text-gray-600 hover:text-gray-500"
              >
                Reset View
              </button>
            }
          </div>
        </div>

        <!-- Chart Container -->
        <div class="relative h-64 mb-4">
          <canvas
            #chartCanvas
            [attr.data-chart-type]="currentChartType()"
            [attr.data-chart-data]="chartDataJson()"
            [attr.data-chart-options]="chartOptionsJson()"
          ></canvas>
          
          @if (isLoading()) {
            <div class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
          }
        </div>

        <!-- Chart Legend -->
        @if (chartData() && chartData()?.datasets && chartData()!.datasets.length > 0) {
          <div class="flex flex-wrap gap-2 mb-4">
            @for (dataset of chartData()!.datasets; track dataset.label) {
              <div class="flex items-center space-x-2">
                <div 
                  class="w-3 h-3 rounded-full"
                  [style.background-color]="getDatasetColor(dataset, 0)"
                ></div>
                <span class="text-sm text-gray-600">{{ dataset.label }}</span>
              </div>
            }
          </div>
        }

        <!-- Chart Statistics -->
        @if (chartStats().length > 0) {
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            @for (stat of chartStats(); track stat.label) {
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">{{ stat.value }}</div>
                <div class="text-sm text-gray-500">{{ stat.label }}</div>
              </div>
            }
          </div>
        }

        <!-- Drill Down Data -->
        @if (drillDownData().length > 0) {
          <div class="mt-6 border-t border-gray-200 pt-4">
            <h4 class="text-md font-medium text-gray-900 mb-3">
              {{ drillDownTitle() }}
            </h4>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    @for (header of drillDownHeaders(); track header) {
                      <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {{ header }}
                      </th>
                    }
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  @for (row of drillDownData(); track $index) {
                    <tr class="hover:bg-gray-50">
                      @for (cell of row; track $index) {
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {{ cell }}
                        </td>
                      }
                    </tr>
                  }
                </tbody>
              </table>
            </div>
          </div>
        }
      </div>
    </div>
  `,
  styles: []
})
export class ChartComponent implements OnInit, OnChanges {
  @Input() data: any[] = [];
  @Input() type: 'bar' | 'line' | 'pie' | 'doughnut' = 'bar';
  @Input() title: string = 'Chart';
  @Input() showDrillDown: boolean = false;
  @Input() drillDownCallback?: (data: any) => any[];

  // Signals
  chartData = signal<ChartData | null>(null);
  currentChartType = signal<'bar' | 'line' | 'pie' | 'doughnut'>('bar');
  isLoading = signal(false);
  drillDownData = signal<any[]>([]);
  drillDownTitle = signal('');

  // Computed properties
  chartTitle = computed(() => this.title);
  chartDataJson = computed(() => JSON.stringify(this.chartData()));
  chartOptionsJson = computed(() => JSON.stringify(this.getChartOptions()));
  chartStats = computed(() => this.calculateStats());
  drillDownHeaders = computed(() => this.getDrillDownHeaders());

  private chartInstance: any = null;

  ngOnInit() {
    this.currentChartType.set(this.type);
    this.processData();
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['data'] || changes['type']) {
      this.processData();
    }
  }

  processData() {
    if (!this.data || this.data.length === 0) {
      this.chartData.set(null);
      return;
    }

    this.isLoading.set(true);

    // Simulate processing delay
    setTimeout(() => {
      const processedData = this.transformDataForChart();
      this.chartData.set(processedData);
      this.isLoading.set(false);
    }, 300);
  }

  transformDataForChart(): ChartData {
    const chartType = this.currentChartType();
    
    switch (chartType) {
      case 'pie':
      case 'doughnut':
        return this.transformForPieChart();
      case 'line':
        return this.transformForLineChart();
      default:
        return this.transformForBarChart();
    }
  }

  transformForBarChart(): ChartData {
    const labels = this.data.map(item => item.label || item.name || `Item ${item.id}`);
    const values = this.data.map(item => item.value || item.count || 0);
    
    return {
      labels,
      datasets: [{
        label: 'Values',
        data: values,
        backgroundColor: this.generateColors(values.length, 0.7),
        borderColor: this.generateColors(values.length, 1),
        borderWidth: 1
      }]
    };
  }

  transformForLineChart(): ChartData {
    const labels = this.data.map(item => item.label || item.name || `Item ${item.id}`);
    const values = this.data.map(item => item.value || item.count || 0);
    
    return {
      labels,
      datasets: [{
        label: 'Trend',
        data: values,
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        fill: true
      }]
    };
  }

  transformForPieChart(): ChartData {
    const labels = this.data.map(item => item.label || item.name || `Item ${item.id}`);
    const values = this.data.map(item => item.value || item.count || 0);
    
    return {
      labels,
      datasets: [{
        label: 'Distribution',
        data: values,
        backgroundColor: this.generateColors(values.length, 0.7),
        borderColor: this.generateColors(values.length, 1),
        borderWidth: 2
      }]
    };
  }

  generateColors(count: number, alpha: number): string[] {
    const colors = [
      `rgba(59, 130, 246, ${alpha})`,   // Blue
      `rgba(16, 185, 129, ${alpha})`,   // Green
      `rgba(245, 101, 101, ${alpha})`,  // Red
      `rgba(251, 191, 36, ${alpha})`,   // Yellow
      `rgba(139, 92, 246, ${alpha})`,   // Purple
      `rgba(236, 72, 153, ${alpha})`,   // Pink
      `rgba(6, 182, 212, ${alpha})`,    // Cyan
      `rgba(34, 197, 94, ${alpha})`     // Emerald
    ];
    
    const result = [];
    for (let i = 0; i < count; i++) {
      result.push(colors[i % colors.length]);
    }
    return result;
  }

  getChartOptions(): ChartOptions {
    const baseOptions: ChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'bottom'
        },
        title: {
          display: true,
          text: this.chartTitle()
        }
      }
    };

    if (this.currentChartType() === 'pie' || this.currentChartType() === 'doughnut') {
      return baseOptions;
    }

    return {
      ...baseOptions,
      scales: {
        y: {
          beginAtZero: true
        },
        x: {
          beginAtZero: true
        }
      }
    };
  }

  calculateStats(): {label: string, value: string}[] {
    if (!this.data || this.data.length === 0) {
      return [];
    }

    const values = this.data.map(item => item.value || item.count || 0);
    const total = values.reduce((sum, val) => sum + val, 0);
    const average = total / values.length;
    const max = Math.max(...values);
    const min = Math.min(...values);

    return [
      { label: 'Total', value: total.toString() },
      { label: 'Average', value: average.toFixed(1) },
      { label: 'Max', value: max.toString() },
      { label: 'Min', value: min.toString() }
    ];
  }

  toggleChartType() {
    const types: ('bar' | 'line' | 'pie' | 'doughnut')[] = ['bar', 'line', 'pie', 'doughnut'];
    const currentIndex = types.indexOf(this.currentChartType());
    const nextIndex = (currentIndex + 1) % types.length;
    this.currentChartType.set(types[nextIndex]);
    this.processData();
  }

  getChartTypeLabel(): string {
    const labels = {
      'bar': 'Switch to Line',
      'line': 'Switch to Pie',
      'pie': 'Switch to Doughnut',
      'doughnut': 'Switch to Bar'
    };
    return labels[this.currentChartType()];
  }

  getDatasetColor(dataset: ChartDataset, index: number): string {
    if (Array.isArray(dataset.backgroundColor)) {
      return dataset.backgroundColor[index] || '#3B82F6';
    }
    return dataset.backgroundColor || '#3B82F6';
  }

  onChartClick(event: any) {
    if (!this.showDrillDown || !this.drillDownCallback) {
      return;
    }

    const clickedData = event.data;
    if (clickedData && this.drillDownCallback) {
      const drillDownResults = this.drillDownCallback(clickedData);
      this.drillDownData.set(drillDownResults);
      this.drillDownTitle.set(`Details for ${clickedData.label || 'Selected Item'}`);
    }
  }

  resetDrillDown() {
    this.drillDownData.set([]);
    this.drillDownTitle.set('');
  }

  getDrillDownHeaders(): string[] {
    if (this.drillDownData().length === 0) {
      return [];
    }

    const firstRow = this.drillDownData()[0];
    return Object.keys(firstRow);
  }
}
