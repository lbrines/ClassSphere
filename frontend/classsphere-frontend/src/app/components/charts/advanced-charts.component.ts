import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApexChartComponent } from './apex-chart.component';
import { ApexChartData } from './apex-chart.component';

@Component({
  selector: 'app-advanced-charts',
  standalone: true,
  imports: [CommonModule, FormsModule, ApexChartComponent],
  template: `
    <div class="px-4 py-6 sm:px-0">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Gráficos Avanzados</h1>
        <p class="mt-2 text-gray-600">
          Visualizaciones interactivas con funcionalidades de drill-down y exportación
        </p>
      </div>

      <!-- Chart Controls -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Controles de Visualización</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Datos</label>
              <select
                [(ngModel)]="selectedDataType"
                (change)="updateChartData()"
                class="w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="courses">Cursos</option>
                <option value="students">Estudiantes</option>
                <option value="assignments">Tareas</option>
                <option value="grades">Calificaciones</option>
                <option value="performance">Rendimiento</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Período</label>
              <select
                [(ngModel)]="selectedPeriod"
                (change)="updateChartData()"
                class="w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="week">Esta Semana</option>
                <option value="month">Este Mes</option>
                <option value="semester">Este Semestre</option>
                <option value="year">Este Año</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Filtros</label>
              <div class="flex space-x-2">
                <button
                  (click)="toggleFilter('active')"
                  [class]="getFilterButtonClass('active')"
                  class="px-3 py-1 text-sm rounded-md"
                >
                  Activos
                </button>
                <button
                  (click)="toggleFilter('completed')"
                  [class]="getFilterButtonClass('completed')"
                  class="px-3 py-1 text-sm rounded-md"
                >
                  Completados
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Main Chart -->
        <div class="lg:col-span-2">
          <app-apex-chart
            [data]="mainChartData()"
            [height]="400"
            [showDrillDown]="true"
            [showExport]="true"
          ></app-apex-chart>
        </div>

        <!-- Secondary Charts -->
        <div>
          <app-apex-chart
            [data]="secondaryChartData1()"
            [height]="300"
            [showDrillDown]="false"
            [showExport]="true"
          ></app-apex-chart>
        </div>

        <div>
          <app-apex-chart
            [data]="secondaryChartData2()"
            [height]="300"
            [showDrillDown]="false"
            [showExport]="true"
          ></app-apex-chart>
        </div>
      </div>

      <!-- Chart Insights -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Insights y Análisis</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            @for (insight of getInsights(); track insight.title) {
              <div class="p-4 bg-gray-50 rounded-lg">
                <h4 class="font-medium text-gray-900 mb-2">{{ insight.title }}</h4>
                <p class="text-sm text-gray-600 mb-2">{{ insight.description }}</p>
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium" [class]="insight.trendClass">
                    {{ insight.trend }}
                  </span>
                  <span class="text-xs text-gray-500">{{ insight.period }}</span>
                </div>
              </div>
            }
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class AdvancedChartsComponent implements OnInit {
  selectedDataType = signal<string>('courses');
  selectedPeriod = signal<string>('month');
  activeFilters = signal<Set<string>>(new Set(['active']));

  mainChartData = signal<ApexChartData | null>(null);
  secondaryChartData1 = signal<ApexChartData | null>(null);
  secondaryChartData2 = signal<ApexChartData | null>(null);

  constructor() {}

  ngOnInit(): void {
    this.updateChartData();
  }

  updateChartData(): void {
    const dataType = this.selectedDataType();
    const period = this.selectedPeriod();
    const filters = this.activeFilters();

    // Generate mock data based on selections
    this.mainChartData.set(this.generateMainChartData(dataType, period, filters));
    this.secondaryChartData1.set(this.generateSecondaryChartData1(dataType, period, filters));
    this.secondaryChartData2.set(this.generateSecondaryChartData2(dataType, period, filters));
  }

  toggleFilter(filter: string): void {
    const filters = new Set(this.activeFilters());
    if (filters.has(filter)) {
      filters.delete(filter);
    } else {
      filters.add(filter);
    }
    this.activeFilters.set(filters);
    this.updateChartData();
  }

  getFilterButtonClass(filter: string): string {
    const isActive = this.activeFilters().has(filter);
    return isActive
      ? 'bg-indigo-600 text-white'
      : 'bg-gray-200 text-gray-700 hover:bg-gray-300';
  }

  generateMainChartData(dataType: string, period: string, filters: Set<string>): ApexChartData {
    const baseData = this.getBaseData(dataType, period);
    
    return {
      title: this.getChartTitle(dataType, period),
      subtitle: `Datos del ${this.getPeriodLabel(period)}`,
      labels: baseData.labels,
      series: baseData.series,
      type: 'bar',
      colors: this.getColorsForDataType(dataType),
      drillDownData: this.generateDrillDownData(dataType, baseData)
    };
  }

  generateSecondaryChartData1(dataType: string, period: string, filters: Set<string>): ApexChartData {
    const baseData = this.getBaseData(dataType, period);
    
    return {
      title: `Distribución ${this.getDataTypeLabel(dataType)}`,
      subtitle: 'Por categoría',
      labels: baseData.labels.slice(0, 5),
      series: baseData.series.slice(0, 5),
      type: 'pie',
      colors: this.getColorsForDataType(dataType)
    };
  }

  generateSecondaryChartData2(dataType: string, period: string, filters: Set<string>): ApexChartData {
    const baseData = this.getBaseData(dataType, period);
    
    return {
      title: `Tendencia ${this.getDataTypeLabel(dataType)}`,
      subtitle: 'Evolución temporal',
      labels: this.getTimeLabels(period),
      series: [{
        name: this.getDataTypeLabel(dataType),
        data: this.generateTimeSeriesData(baseData.series.length)
      }],
      type: 'line',
      colors: this.getColorsForDataType(dataType)
    };
  }

  getBaseData(dataType: string, period: string) {
    const dataSets = {
      courses: {
        labels: ['Matemáticas 101', 'Física 201', 'Álgebra Lineal', 'Cálculo', 'Estadística'],
        series: [25, 18, 22, 30, 15]
      },
      students: {
        labels: ['Activos', 'Inactivos', 'Graduados', 'En Riesgo', 'Destacados'],
        series: [120, 15, 45, 12, 8]
      },
      assignments: {
        labels: ['Completadas', 'Pendientes', 'En Revisión', 'Calificadas', 'Vencidas'],
        series: [85, 25, 10, 75, 5]
      },
      grades: {
        labels: ['A (90-100)', 'B (80-89)', 'C (70-79)', 'D (60-69)', 'F (<60)'],
        series: [35, 45, 25, 10, 5]
      },
      performance: {
        labels: ['Excelente', 'Bueno', 'Regular', 'Necesita Mejora', 'Crítico'],
        series: [20, 35, 30, 12, 3]
      }
    };

    return dataSets[dataType as keyof typeof dataSets] || dataSets.courses;
  }

  generateDrillDownData(dataType: string, baseData: any) {
    const drillDownData: { [key: string]: ApexChartData } = {};

    baseData.labels.forEach((label: string, index: number) => {
      drillDownData[label] = {
        title: `Detalle: ${label}`,
        subtitle: 'Información específica',
        labels: this.generateDrillDownLabels(dataType, label),
        series: this.generateDrillDownSeries(dataType, label, baseData.series[index]),
        type: 'bar',
        colors: this.getColorsForDataType(dataType)
      };
    });

    return drillDownData;
  }

  generateDrillDownLabels(dataType: string, parentLabel: string): string[] {
    const drillDownLabels = {
      courses: ['Estudiantes Activos', 'Tareas Asignadas', 'Calificaciones', 'Participación'],
      students: ['Cursos Inscritos', 'Tareas Completadas', 'Promedio', 'Asistencia'],
      assignments: ['Enviadas', 'Pendientes', 'Calificadas', 'En Revisión'],
      grades: ['Primer Parcial', 'Segundo Parcial', 'Final', 'Proyectos'],
      performance: ['Tareas', 'Exámenes', 'Participación', 'Proyectos']
    };

    return drillDownLabels[dataType as keyof typeof drillDownLabels] || drillDownLabels.courses;
  }

  generateDrillDownSeries(dataType: string, parentLabel: string, parentValue: number): number[] {
    // Generate proportional drill-down data
    const labels = this.generateDrillDownLabels(dataType, parentLabel);
    const total = parentValue;
    const series: number[] = [];
    
    for (let i = 0; i < labels.length; i++) {
      const value = Math.floor(total * (0.2 + Math.random() * 0.3));
      series.push(value);
    }
    
    return series;
  }

  generateTimeSeriesData(length: number): number[] {
    const data: number[] = [];
    for (let i = 0; i < 7; i++) {
      data.push(Math.floor(Math.random() * 50) + 20);
    }
    return data;
  }

  getTimeLabels(period: string): string[] {
    const timeLabels = {
      week: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
      month: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
      semester: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
      year: ['Q1', 'Q2', 'Q3', 'Q4']
    };

    return timeLabels[period as keyof typeof timeLabels] || timeLabels.month;
  }

  getChartTitle(dataType: string, period: string): string {
    const dataTypeLabels = {
      courses: 'Cursos',
      students: 'Estudiantes',
      assignments: 'Tareas',
      grades: 'Calificaciones',
      performance: 'Rendimiento'
    };

    const periodLabels = {
      week: 'Esta Semana',
      month: 'Este Mes',
      semester: 'Este Semestre',
      year: 'Este Año'
    };

    return `${dataTypeLabels[dataType as keyof typeof dataTypeLabels]} - ${periodLabels[period as keyof typeof periodLabels]}`;
  }

  getDataTypeLabel(dataType: string): string {
    const labels = {
      courses: 'Cursos',
      students: 'Estudiantes',
      assignments: 'Tareas',
      grades: 'Calificaciones',
      performance: 'Rendimiento'
    };

    return labels[dataType as keyof typeof labels] || 'Datos';
  }

  getPeriodLabel(period: string): string {
    const labels = {
      week: 'última semana',
      month: 'último mes',
      semester: 'último semestre',
      year: 'último año'
    };

    return labels[period as keyof typeof labels] || 'período actual';
  }

  getColorsForDataType(dataType: string): string[] {
    const colorSets = {
      courses: ['#3B82F6', '#1D4ED8', '#1E40AF', '#1E3A8A', '#312E81'],
      students: ['#10B981', '#059669', '#047857', '#065F46', '#064E3B'],
      assignments: ['#F59E0B', '#D97706', '#B45309', '#92400E', '#78350F'],
      grades: ['#EF4444', '#DC2626', '#B91C1C', '#991B1B', '#7F1D1D'],
      performance: ['#8B5CF6', '#7C3AED', '#6D28D9', '#5B21B6', '#4C1D95']
    };

    return colorSets[dataType as keyof typeof colorSets] || colorSets.courses;
  }

  getInsights() {
    const dataType = this.selectedDataType();
    const period = this.selectedPeriod();

    const insights = {
      courses: [
        {
          title: 'Cursos Más Populares',
          description: 'Matemáticas 101 tiene la mayor inscripción',
          trend: '+15%',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        },
        {
          title: 'Tasa de Completación',
          description: '85% de los cursos están completos',
          trend: '+5%',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        },
        {
          title: 'Nuevos Cursos',
          description: '3 nuevos cursos agregados este mes',
          trend: '+3',
          trendClass: 'text-blue-600',
          period: 'este mes'
        }
      ],
      students: [
        {
          title: 'Crecimiento Estudiantil',
          description: 'Aumento constante en inscripciones',
          trend: '+12%',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        },
        {
          title: 'Estudiantes en Riesgo',
          description: '12 estudiantes requieren atención',
          trend: '-2',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        },
        {
          title: 'Tasa de Retención',
          description: '92% de estudiantes activos',
          trend: '+3%',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        }
      ],
      assignments: [
        {
          title: 'Tareas Completadas',
          description: '85% de tareas entregadas a tiempo',
          trend: '+8%',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        },
        {
          title: 'Tiempo Promedio',
          description: '3.2 días promedio de entrega',
          trend: '-0.5 días',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        },
        {
          title: 'Calidad de Entregas',
          description: 'Mejora en calidad de trabajos',
          trend: '+15%',
          trendClass: 'text-green-600',
          period: 'vs mes anterior'
        }
      ]
    };

    return insights[dataType as keyof typeof insights] || insights.courses;
  }
}
