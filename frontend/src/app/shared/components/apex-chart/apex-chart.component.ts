import { AfterViewInit, Component, ElementRef, Input, OnChanges, OnDestroy, SimpleChanges, ViewChild } from '@angular/core';
import ApexCharts, { ApexOptions } from 'apexcharts';

import { ChartData, ChartPoint } from '../../../core/models/classroom.model';

@Component({
  selector: 'app-apex-chart',
  standalone: true,
  template: `<div #chartHost class="w-full"></div>`,
})
export class ApexChartComponent implements AfterViewInit, OnChanges, OnDestroy {
  @Input({ required: true }) chart!: ChartData;

  @ViewChild('chartHost', { static: true })
  private chartHost!: ElementRef<HTMLDivElement>;

  private instance?: ApexCharts;

  ngAfterViewInit(): void {
    this.render();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['chart'] && !changes['chart'].firstChange) {
      this.update();
    }
  }

  ngOnDestroy(): void {
    this.instance?.destroy();
  }

  protected createChart(element: HTMLElement, options: ApexOptions): ApexCharts {
    return new ApexCharts(element, options);
  }

  private render(): void {
    if (!this.chartHost || !this.chart) {
      return;
    }
    this.instance = this.createChart(this.chartHost.nativeElement, this.buildOptions(this.chart));
    void this.instance.render();
  }

  private update(): void {
    if (!this.instance || !this.chart) {
      return;
    }
    const options = this.buildOptions(this.chart);
    void this.instance.updateOptions(options, true, true);
  }

  private buildOptions(chart: ChartData): ApexOptions {
    if (chart.type === 'donut') {
      const donutSeries = chart.series[0]?.data ?? [];
      return {
        chart: {
          type: 'donut',
          background: 'transparent',
        },
        labels: donutSeries.map((point) => String(point.x)),
        series: donutSeries.map((point) => point.y),
        dataLabels: {
          style: { colors: ['#0f172a'] },
        },
        legend: {
          labels: { colors: '#cbd5f5' },
        },
        theme: {
          mode: 'dark',
        },
      };
    }

    const series = chart.series.map((serie) => ({
      name: serie.name,
      data: serie.data.map((point) => this.normalizePoint(point)),
    }));

    return {
      chart: {
        type: chart.type,
        background: 'transparent',
        toolbar: { show: false },
        fontFamily: 'Inter, sans-serif',
        animations: { enabled: true },
      },
      theme: {
        mode: 'dark',
      },
      colors: ['#38bdf8', '#818cf8', '#f97316', '#facc15'],
      stroke: {
        curve: chart.type === 'area' || chart.type === 'line' ? 'smooth' : 'straight',
        width: 2,
      },
      dataLabels: {
        enabled: false,
      },
      fill: {
        type: chart.type === 'area' ? 'gradient' : 'solid',
        gradient: {
          shadeIntensity: 1,
          opacityFrom: 0.35,
          opacityTo: 0.05,
          stops: [0, 90, 100],
        },
      },
      series,
      xaxis: chart.categories?.length
        ? {
            categories: chart.categories,
            labels: { style: { colors: '#cbd5f5' } },
          }
        : {
            labels: { style: { colors: '#cbd5f5' } },
          },
      yaxis: {
        labels: { style: { colors: '#cbd5f5' } },
      },
      grid: {
        borderColor: '#1e293b',
        strokeDashArray: 4,
      },
      legend: {
        labels: { colors: '#cbd5f5' },
      },
      tooltip: {
        theme: 'dark',
      },
    };
  }

  private normalizePoint(point: ChartPoint): { x: string | number; y: number } {
    return {
      x: point.x,
      y: point.y,
    };
  }
}
