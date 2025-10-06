import { Component, Input, Output, EventEmitter, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ExportService, ExportOptions } from '../../services/export.service';

@Component({
  selector: 'app-export-panel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">Exportar Datos</h3>
          <button
            (click)="togglePanel()"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    [attr.d]="isExpanded() ? 'M19 9l-7 7-7-7' : 'M9 5l7 7-7 7'"></path>
            </svg>
          </button>
        </div>

        @if (isExpanded()) {
          <div class="space-y-4">
            <!-- Export Format Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Formato de Exportación</label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
                <button
                  *ngFor="let format of exportFormats"
                  (click)="selectFormat(format.value)"
                  [class]="getFormatButtonClass(format.value)"
                  class="px-3 py-2 text-sm rounded-md border transition-colors"
                >
                  {{ format.icon }} {{ format.label }}
                </button>
              </div>
            </div>

            <!-- Export Options -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del archivo</label>
                <input
                  type="text"
                  [(ngModel)]="exportOptions.filename"
                  class="w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="nombre-del-archivo"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Calidad</label>
                <select
                  [(ngModel)]="exportOptions.quality"
                  class="w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option [value]="0.8">Baja (80%)</option>
                  <option [value]="0.9">Media (90%)</option>
                  <option [value]="0.95">Alta (95%)</option>
                  <option [value]="1.0">Máxima (100%)</option>
                </select>
              </div>
            </div>

            <!-- Advanced Options -->
            <div class="border-t pt-4">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-gray-700">Opciones Avanzadas</span>
                <button
                  (click)="toggleAdvancedOptions()"
                  class="text-sm text-indigo-600 hover:text-indigo-800"
                >
                  {{ showAdvancedOptions() ? 'Ocultar' : 'Mostrar' }}
                </button>
              </div>

              @if (showAdvancedOptions()) {
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Escala</label>
                    <input
                      type="range"
                      min="1"
                      max="3"
                      step="0.5"
                      [(ngModel)]="exportOptions.scale"
                      class="w-full"
                    >
                    <div class="text-xs text-gray-500 mt-1">{{ exportOptions.scale }}x</div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Color de fondo</label>
                    <input
                      type="color"
                      [(ngModel)]="exportOptions.backgroundColor"
                      class="w-full h-10 border border-gray-300 rounded-md"
                    >
                  </div>
                </div>
              }
            </div>

            <!-- Export Actions -->
            <div class="flex flex-wrap gap-2 pt-4 border-t">
              <button
                (click)="exportDashboard()"
                [disabled]="isExporting()"
                class="flex items-center px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                @if (isExporting()) {
                  <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                } @else {
                  📊
                }
                Exportar Dashboard
              </button>

              <button
                (click)="exportCharts()"
                [disabled]="isExporting()"
                class="flex items-center px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                📈 Exportar Gráficos
              </button>

              <button
                (click)="exportData()"
                [disabled]="isExporting()"
                class="flex items-center px-4 py-2 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                📋 Exportar Datos
              </button>

              <button
                (click)="exportAll()"
                [disabled]="isExporting()"
                class="flex items-center px-4 py-2 bg-gray-600 text-white text-sm rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                📦 Exportar Todo
              </button>
            </div>

            <!-- Export Status -->
            @if (exportStatus()) {
              <div class="mt-4 p-3 rounded-md" [class]="getStatusClass()">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    @if (exportStatus()?.success) {
                      <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                      </svg>
                    } @else {
                      <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                      </svg>
                    }
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium" [class]="getStatusTextClass()">
                      {{ exportStatus()?.message }}
                    </p>
                    @if (exportStatus()?.filename) {
                      <p class="text-xs text-gray-500 mt-1">
                        Archivo: {{ exportStatus()?.filename }}
                      </p>
                    }
                  </div>
                </div>
              </div>
            }
          </div>
        }
      </div>
    </div>
  `,
  styles: []
})
export class ExportPanelComponent {
  @Input() dashboardElement?: HTMLElement;
  @Input() chartElements?: HTMLElement[];
  @Input() dashboardData?: any;
  @Input() chartData?: any[];

  @Output() exportComplete = new EventEmitter<{ success: boolean; filename?: string; error?: string }>();

  isExpanded = signal(false);
  showAdvancedOptions = signal(false);
  isExporting = signal(false);
  exportStatus = signal<{ success: boolean; message: string; filename?: string } | null>(null);

  exportOptions: ExportOptions = {
    format: 'pdf',
    filename: 'dashboard-export',
    quality: 0.9,
    scale: 2,
    backgroundColor: '#ffffff',
    includeTimestamp: true
  };

  exportFormats = [
    { value: 'pdf', label: 'PDF', icon: '📄' },
    { value: 'png', label: 'PNG', icon: '🖼️' },
    { value: 'svg', label: 'SVG', icon: '📐' }
  ];

  constructor(private exportService: ExportService) {}

  togglePanel(): void {
    this.isExpanded.update(expanded => !expanded);
  }

  toggleAdvancedOptions(): void {
    this.showAdvancedOptions.update(show => !show);
  }

  selectFormat(format: string): void {
    this.exportOptions.format = format as 'pdf' | 'png' | 'svg';
  }

  getFormatButtonClass(format: string): string {
    const isSelected = this.exportOptions.format === format;
    return isSelected
      ? 'bg-indigo-600 text-white border-indigo-600'
      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50';
  }

  getStatusClass(): string {
    const status = this.exportStatus();
    if (!status) return '';
    return status.success ? 'bg-green-50' : 'bg-red-50';
  }

  getStatusTextClass(): string {
    const status = this.exportStatus();
    if (!status) return '';
    return status.success ? 'text-green-800' : 'text-red-800';
  }

  async exportDashboard(): Promise<void> {
    if (!this.dashboardElement) {
      this.setStatus(false, 'No hay elemento de dashboard para exportar');
      return;
    }

    this.isExporting.set(true);
    this.clearStatus();

    try {
      const result = await this.performExport(this.dashboardElement, 'dashboard');
      this.setStatus(result.success, result.success ? 'Dashboard exportado exitosamente' : result.error || 'Error desconocido', result.filename);
      this.exportComplete.emit(result);
    } catch (error) {
      this.setStatus(false, 'Error al exportar dashboard');
      this.exportComplete.emit({ success: false, error: 'Error al exportar dashboard' });
    } finally {
      this.isExporting.set(false);
    }
  }

  async exportCharts(): Promise<void> {
    if (!this.chartElements || this.chartElements.length === 0) {
      this.setStatus(false, 'No hay gráficos para exportar');
      return;
    }

    this.isExporting.set(true);
    this.clearStatus();

    try {
      if (this.exportOptions.format === 'pdf' && this.chartElements.length > 1) {
        const result = await this.exportService.exportMultipleToPDF(this.chartElements, this.exportOptions);
        this.setStatus(result.success, result.success ? 'Gráficos exportados exitosamente' : result.error || 'Error desconocido', result.filename);
        this.exportComplete.emit(result);
      } else {
        const result = await this.performExport(this.chartElements[0], 'charts');
        this.setStatus(result.success, result.success ? 'Gráfico exportado exitosamente' : result.error || 'Error desconocido', result.filename);
        this.exportComplete.emit(result);
      }
    } catch (error) {
      this.setStatus(false, 'Error al exportar gráficos');
      this.exportComplete.emit({ success: false, error: 'Error al exportar gráficos' });
    } finally {
      this.isExporting.set(false);
    }
  }

  exportData(): void {
    if (!this.dashboardData && !this.chartData) {
      this.setStatus(false, 'No hay datos para exportar');
      return;
    }

    this.clearStatus();

    try {
      let result;
      if (this.chartData && this.chartData.length > 0) {
        result = this.exportService.exportChartDataAsCSV(this.chartData, 'chart-data');
      } else if (this.dashboardData) {
        result = this.exportService.exportDashboardData(this.dashboardData, 'dashboard-data');
      } else {
        this.setStatus(false, 'No hay datos válidos para exportar');
        return;
      }

      this.setStatus(result.success, result.success ? 'Datos exportados exitosamente' : result.error || 'Error desconocido', result.filename);
      this.exportComplete.emit(result);
    } catch (error) {
      this.setStatus(false, 'Error al exportar datos');
      this.exportComplete.emit({ success: false, error: 'Error al exportar datos' });
    }
  }

  async exportAll(): Promise<void> {
    this.isExporting.set(true);
    this.clearStatus();

    try {
      const results = [];
      
      // Export dashboard
      if (this.dashboardElement) {
        const dashboardResult = await this.performExport(this.dashboardElement, 'dashboard');
        results.push(dashboardResult);
      }

      // Export charts
      if (this.chartElements && this.chartElements.length > 0) {
        if (this.exportOptions.format === 'pdf' && this.chartElements.length > 1) {
          const chartsResult = await this.exportService.exportMultipleToPDF(this.chartElements, this.exportOptions);
          results.push(chartsResult);
        } else {
          const chartResult = await this.performExport(this.chartElements[0], 'charts');
          results.push(chartResult);
        }
      }

      // Export data
      if (this.dashboardData || this.chartData) {
        const dataResult = this.exportData();
        if (dataResult) {
          results.push(dataResult);
        }
      }

      const successCount = results.filter(r => r.success).length;
      const totalCount = results.length;

      this.setStatus(
        successCount === totalCount,
        `${successCount}/${totalCount} exportaciones completadas exitosamente`
      );

      this.exportComplete.emit({
        success: successCount === totalCount,
        filename: `${this.exportOptions.filename}-complete`
      });
    } catch (error) {
      this.setStatus(false, 'Error al exportar todos los elementos');
      this.exportComplete.emit({ success: false, error: 'Error al exportar todos los elementos' });
    } finally {
      this.isExporting.set(false);
    }
  }

  private async performExport(element: HTMLElement, type: string): Promise<{ success: boolean; filename?: string; error?: string }> {
    const options = { ...this.exportOptions, filename: `${this.exportOptions.filename}-${type}` };

    switch (this.exportOptions.format) {
      case 'pdf':
        return await this.exportService.exportToPDF(element, options);
      case 'png':
        return await this.exportService.exportToPNG(element, options);
      case 'svg':
        return await this.exportService.exportToSVG(element, options);
      default:
        throw new Error('Formato de exportación no soportado');
    }
  }

  private setStatus(success: boolean, message: string, filename?: string): void {
    this.exportStatus.set({ success, message, filename });
    
    // Clear status after 5 seconds
    setTimeout(() => {
      this.clearStatus();
    }, 5000);
  }

  private clearStatus(): void {
    this.exportStatus.set(null);
  }
}
