import { Component, OnInit, Input, signal, computed, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgApexchartsModule, ChartComponent } from 'ng-apexcharts';
import { ApexOptions } from 'ng-apexcharts';

export interface ApexChartData {
  labels: string[];
  series: number[] | { name: string; data: number[] }[];
  type?: 'line' | 'area' | 'bar' | 'histogram' | 'pie' | 'donut' | 'radialBar' | 'scatter' | 'bubble' | 'heatmap' | 'treemap' | 'boxPlot' | 'candlestick' | 'radar' | 'polarArea' | 'rangeBar';
  colors?: string[];
  title?: string;
  subtitle?: string;
  drillDownData?: { [key: string]: ApexChartData };
}

@Component({
  selector: 'app-apex-chart',
  standalone: true,
  imports: [CommonModule, FormsModule, NgApexchartsModule],
  template: `
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <!-- Chart Header -->
        <div class="flex justify-between items-center mb-4">
          <div>
            <h3 class="text-lg font-medium text-gray-900">
              {{ chartData()?.title || 'Gráfico' }}
            </h3>
            @if (chartData()?.subtitle) {
              <p class="text-sm text-gray-500">{{ chartData()?.subtitle }}</p>
            }
          </div>
          <div class="flex items-center space-x-2">
            <!-- Chart Type Selector -->
            <select
              [(ngModel)]="selectedChartType"
              (change)="updateChartType()"
              class="text-sm border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="bar">Barras</option>
              <option value="line">Línea</option>
              <option value="area">Área</option>
              <option value="pie">Circular</option>
              <option value="donut">Dona</option>
            </select>
            
            <!-- Export Options -->
            <button
              (click)="exportChart('png')"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              📊 PNG
            </button>
            <button
              (click)="exportChart('svg')"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              📈 SVG
            </button>
          </div>
        </div>

        <!-- Chart Container -->
        <div class="relative">
          @if (isLoading()) {
            <div class="flex justify-center items-center h-64">
              <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
            </div>
          } @else if (errorMessage()) {
            <div class="rounded-md bg-red-50 p-4">
              <div class="text-sm text-red-700">
                {{ errorMessage() }}
              </div>
            </div>
          } @else if (chartOptions && chartOptions.series) {
            <apx-chart
              #chart
              [series]="chartOptions.series || []"
              [chart]="chartOptions.chart || { type: 'line', height: 350 }"
              [labels]="chartOptions.labels || []"
              [colors]="chartOptions.colors || []"
              [xaxis]="chartOptions.xaxis || {}"
              [yaxis]="chartOptions.yaxis || {}"
              [title]="chartOptions.title || {}"
              [subtitle]="chartOptions.subtitle || {}"
              [legend]="chartOptions.legend || {}"
              [tooltip]="chartOptions.tooltip || {}"
              [plotOptions]="chartOptions.plotOptions || {}"
              [dataLabels]="chartOptions.dataLabels || {}"
              [stroke]="chartOptions.stroke || {}"
              [fill]="chartOptions.fill || {}"
              [responsive]="chartOptions.responsive || []"
              (dataPointSelection)="onDataPointSelection($event)"
            ></apx-chart>
          }
        </div>

        <!-- Chart Statistics -->
        @if (chartStats().length > 0) {
          <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            @for (stat of chartStats(); track stat.label) {
              <div class="text-center">
                <div class="text-2xl font-bold" [class]="stat.colorClass">
                  {{ stat.value }}
                </div>
                <div class="text-sm text-gray-500">{{ stat.label }}</div>
              </div>
            }
          </div>
        }

        <!-- Drill Down Navigation -->
        @if (drillDownPath().length > 0) {
          <div class="mt-4 flex items-center space-x-2 text-sm text-gray-600">
            <span>Navegación:</span>
            @for (path of drillDownPath(); track path; let i = $index) {
              <span>
                @if (i > 0) {
                  <span class="mx-1">></span>
                }
                <button
                  (click)="navigateToDrillDown(i)"
                  class="hover:text-indigo-600 underline"
                >
                  {{ path }}
                </button>
              </span>
            }
            <button
              (click)="resetDrillDown()"
              class="ml-2 text-indigo-600 hover:text-indigo-800"
            >
              [Volver al inicio]
            </button>
          </div>
        }
      </div>
    </div>
  `,
  styles: []
})
export class ApexChartComponent implements OnInit, OnChanges {
  @Input() data: ApexChartData | null = null;
  @Input() height: number = 350;
  @Input() showDrillDown: boolean = true;
  @Input() showExport: boolean = true;

  @ViewChild('chart') chart!: ChartComponent;

  chartData = signal<ApexChartData | null>(null);
  isLoading = signal(false);
  errorMessage = signal('');
  selectedChartType = signal<string>('bar');
  drillDownPath = signal<string[]>([]);
  currentDrillDownKey = signal<string | null>(null);

  chartOptions: ApexOptions = {};

  constructor() {}

  ngOnInit(): void {
    if (this.data) {
      this.chartData.set(this.data);
      this.updateChartOptions();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['data'] && this.data) {
      this.chartData.set(this.data);
      this.updateChartOptions();
    }
  }

  updateChartOptions(): void {
    const data = this.chartData();
    if (!data) return;

    const chartType = this.selectedChartType();
    
    this.chartOptions = {
      series: this.getSeriesData(data),
      chart: {
        type: chartType as any,
        height: this.height,
        toolbar: {
          show: true,
          tools: {
            download: true,
            selection: true,
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: true,
            reset: true
          }
        },
        animations: {
          enabled: true,
          speed: 800
        }
      },
      labels: data.labels,
      colors: data.colors || this.getDefaultColors(),
      xaxis: {
        type: 'category',
        labels: {
          style: {
            colors: '#6B7280'
          }
        }
      },
      yaxis: {
        labels: {
          style: {
            colors: '#6B7280'
          }
        }
      },
      title: {
        text: data.title,
        style: {
          fontSize: '16px',
          fontWeight: 'bold',
          color: '#111827'
        }
      },
      subtitle: {
        text: data.subtitle,
        style: {
          fontSize: '12px',
          color: '#6B7280'
        }
      },
      legend: {
        position: 'bottom',
        horizontalAlign: 'center',
        labels: {
          colors: '#6B7280'
        }
      },
      tooltip: {
        enabled: true,
        shared: true,
        intersect: false,
        style: {
          fontSize: '12px'
        }
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          borderRadius: 4
        },
        pie: {
          donut: {
            size: '70%'
          }
        }
      },
      dataLabels: {
        enabled: chartType === 'pie' || chartType === 'donut',
        style: {
          fontSize: '12px',
          fontWeight: 'bold'
        }
      },
      stroke: {
        show: chartType === 'line' || chartType === 'area',
        curve: 'smooth',
        width: 2
      },
      fill: {
        type: chartType === 'area' ? 'gradient' : 'solid',
        gradient: {
          shade: 'light',
          type: 'vertical',
          shadeIntensity: 0.5,
          gradientToColors: undefined,
          inverseColors: false,
          opacityFrom: 0.8,
          opacityTo: 0.3
        }
      },
      responsive: [
        {
          breakpoint: 768,
          options: {
            chart: {
              height: 300
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
  }

  getSeriesData(data: ApexChartData): any[] {
    if (Array.isArray(data.series) && data.series.length > 0) {
      if (typeof data.series[0] === 'number') {
        return [{ name: 'Datos', data: data.series as number[] }];
      } else {
        return data.series as { name: string; data: number[] }[];
      }
    }
    return [];
  }

  getDefaultColors(): string[] {
    return [
      '#3B82F6', // Blue
      '#10B981', // Green
      '#F59E0B', // Yellow
      '#EF4444', // Red
      '#8B5CF6', // Purple
      '#06B6D4', // Cyan
      '#84CC16', // Lime
      '#F97316'  // Orange
    ];
  }

  updateChartType(): void {
    this.updateChartOptions();
  }

  onDataPointSelection(event: any): void {
    if (!this.showDrillDown) return;

    const data = this.chartData();
    if (!data?.drillDownData) return;

    const seriesIndex = event.seriesIndex;
    const dataPointIndex = event.dataPointIndex;
    const label = data.labels[dataPointIndex];

    // Find drill down data for this label
    const drillDownKey = Object.keys(data.drillDownData).find(key => 
      key.toLowerCase().includes(label.toLowerCase())
    );

    if (drillDownKey && data.drillDownData[drillDownKey]) {
      this.drillDownPath.update(path => [...path, label]);
      this.currentDrillDownKey.set(drillDownKey);
      this.chartData.set(data.drillDownData[drillDownKey]);
      this.updateChartOptions();
    }
  }

  navigateToDrillDown(index: number): void {
    const data = this.chartData();
    if (!data?.drillDownData) return;

    // Reset to original data and navigate to the specified level
    this.drillDownPath.update(path => path.slice(0, index + 1));
    this.updateChartOptions();
  }

  resetDrillDown(): void {
    this.drillDownPath.set([]);
    this.currentDrillDownKey.set(null);
    if (this.data) {
      this.chartData.set(this.data);
      this.updateChartOptions();
    }
  }

  exportChart(format: 'png' | 'svg'): void {
    if (this.chart) {
      this.chart.dataURI().then((result: { imgURI: string; } | { blob: Blob; }) => {
        const uri = 'imgURI' in result ? result.imgURI : URL.createObjectURL(result.blob);
        const link = document.createElement('a');
        link.download = `chart-${Date.now()}.${format}`;
        link.href = uri;
        link.click();
      });
    }
  }

  chartStats() {
    const data = this.chartData();
    if (!data || !data.series) return [];

    const series = Array.isArray(data.series) ? data.series : [data.series];
    const values = series.flatMap(s => typeof s === 'number' ? [s] : s.data);

    if (values.length === 0) return [];

    const total = values.reduce((sum, val) => sum + val, 0);
    const average = total / values.length;
    const max = Math.max(...values);
    const min = Math.min(...values);

    return [
      { label: 'Total', value: total.toLocaleString(), colorClass: 'text-blue-600' },
      { label: 'Promedio', value: average.toFixed(1), colorClass: 'text-green-600' },
      { label: 'Máximo', value: max.toLocaleString(), colorClass: 'text-red-600' },
      { label: 'Mínimo', value: min.toLocaleString(), colorClass: 'text-yellow-600' }
    ];
  }
}
