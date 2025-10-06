import { Injectable } from '@angular/core';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export interface ExportOptions {
  format: 'pdf' | 'png' | 'svg';
  filename?: string;
  quality?: number;
  scale?: number;
  backgroundColor?: string;
  includeTimestamp?: boolean;
}

export interface ExportResult {
  success: boolean;
  filename?: string;
  error?: string;
  data?: any;
}

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  constructor() {}

  /**
   * Export element to PDF
   */
  async exportToPDF(element: HTMLElement, options: ExportOptions = {}): Promise<ExportResult> {
    try {
      const {
        filename = 'export',
        quality = 0.92,
        scale = 2,
        backgroundColor = '#ffffff',
        includeTimestamp = true
      } = options;

      // Generate filename with timestamp if requested
      const finalFilename = includeTimestamp 
        ? `${filename}-${this.getTimestamp()}`
        : filename;

      // Convert element to canvas
      const canvas = await html2canvas(element, {
        scale,
        useCORS: true,
        allowTaint: true,
        backgroundColor,
        logging: false
      });

      // Create PDF
      const imgData = canvas.toDataURL('image/png', quality);
      const pdf = new jsPDF({
        orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      // Calculate dimensions to fit page
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      const ratio = Math.min(pageWidth / imgWidth, pageHeight / imgHeight);
      const finalWidth = imgWidth * ratio;
      const finalHeight = imgHeight * ratio;

      // Add image to PDF
      pdf.addImage(imgData, 'PNG', 0, 0, finalWidth, finalHeight);
      
      // Save PDF
      pdf.save(`${finalFilename}.pdf`);

      return {
        success: true,
        filename: `${finalFilename}.pdf`
      };
    } catch (error) {
      console.error('Error exporting to PDF:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export element to PNG
   */
  async exportToPNG(element: HTMLElement, options: ExportOptions = {}): Promise<ExportResult> {
    try {
      const {
        filename = 'export',
        quality = 0.92,
        scale = 2,
        backgroundColor = '#ffffff',
        includeTimestamp = true
      } = options;

      // Generate filename with timestamp if requested
      const finalFilename = includeTimestamp 
        ? `${filename}-${this.getTimestamp()}`
        : filename;

      // Convert element to canvas
      const canvas = await html2canvas(element, {
        scale,
        useCORS: true,
        allowTaint: true,
        backgroundColor,
        logging: false
      });

      // Convert to PNG and download
      const link = document.createElement('a');
      link.download = `${finalFilename}.png`;
      link.href = canvas.toDataURL('image/png', quality);
      link.click();

      return {
        success: true,
        filename: `${finalFilename}.png`
      };
    } catch (error) {
      console.error('Error exporting to PNG:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export SVG element
   */
  async exportToSVG(element: HTMLElement, options: ExportOptions = {}): Promise<ExportResult> {
    try {
      const {
        filename = 'export',
        includeTimestamp = true
      } = options;

      // Generate filename with timestamp if requested
      const finalFilename = includeTimestamp 
        ? `${filename}-${this.getTimestamp()}`
        : filename;

      // Find SVG element
      const svgElement = element.querySelector('svg') || element;
      
      if (!svgElement || svgElement.tagName.toLowerCase() !== 'svg') {
        throw new Error('No SVG element found');
      }

      // Clone SVG to avoid modifying original
      const svgClone = svgElement.cloneNode(true) as SVGElement;
      
      // Add namespace if not present
      if (!svgClone.getAttribute('xmlns')) {
        svgClone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      }

      // Convert to string
      const svgData = new XMLSerializer().serializeToString(svgClone);
      
      // Create blob and download
      const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
      const svgUrl = URL.createObjectURL(svgBlob);
      
      const link = document.createElement('a');
      link.href = svgUrl;
      link.download = `${finalFilename}.svg`;
      link.click();
      
      // Clean up
      URL.revokeObjectURL(svgUrl);

      return {
        success: true,
        filename: `${finalFilename}.svg`
      };
    } catch (error) {
      console.error('Error exporting to SVG:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export dashboard data as JSON
   */
  exportDashboardData(data: any, filename: string = 'dashboard-data'): ExportResult {
    try {
      const jsonData = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonData], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `${filename}-${this.getTimestamp()}.json`;
      link.click();
      
      URL.revokeObjectURL(url);

      return {
        success: true,
        filename: `${filename}-${this.getTimestamp()}.json`
      };
    } catch (error) {
      console.error('Error exporting dashboard data:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export chart data as CSV
   */
  exportChartDataAsCSV(data: any[], filename: string = 'chart-data'): ExportResult {
    try {
      if (!data || data.length === 0) {
        throw new Error('No data to export');
      }

      // Get headers from first object
      const headers = Object.keys(data[0]);
      
      // Create CSV content
      const csvContent = [
        headers.join(','),
        ...data.map(row => 
          headers.map(header => {
            const value = row[header];
            // Escape values that contain commas or quotes
            if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
              return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
          }).join(',')
        )
      ].join('\n');

      // Create blob and download
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `${filename}-${this.getTimestamp()}.csv`;
      link.click();
      
      URL.revokeObjectURL(url);

      return {
        success: true,
        filename: `${filename}-${this.getTimestamp()}.csv`
      };
    } catch (error) {
      console.error('Error exporting chart data:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Export multiple elements as a combined PDF
   */
  async exportMultipleToPDF(elements: HTMLElement[], options: ExportOptions = {}): Promise<ExportResult> {
    try {
      const {
        filename = 'export',
        quality = 0.92,
        scale = 2,
        backgroundColor = '#ffffff',
        includeTimestamp = true
      } = options;

      const finalFilename = includeTimestamp 
        ? `${filename}-${this.getTimestamp()}`
        : filename;

      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        
        // Convert element to canvas
        const canvas = await html2canvas(element, {
          scale,
          useCORS: true,
          allowTaint: true,
          backgroundColor,
          logging: false
        });

        // Add new page if not first element
        if (i > 0) {
          pdf.addPage();
        }

        // Calculate dimensions to fit page
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const imgWidth = canvas.width;
        const imgHeight = canvas.height;
        const ratio = Math.min(pageWidth / imgWidth, pageHeight / imgHeight);
        const finalWidth = imgWidth * ratio;
        const finalHeight = imgHeight * ratio;

        // Add image to PDF
        const imgData = canvas.toDataURL('image/png', quality);
        pdf.addImage(imgData, 'PNG', 0, 0, finalWidth, finalHeight);
      }

      // Save PDF
      pdf.save(`${finalFilename}.pdf`);

      return {
        success: true,
        filename: `${finalFilename}.pdf`
      };
    } catch (error) {
      console.error('Error exporting multiple elements to PDF:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Get current timestamp for filename
   */
  private getTimestamp(): string {
    const now = new Date();
    return now.toISOString().replace(/[:.]/g, '-').slice(0, -5);
  }

  /**
   * Validate export options
   */
  validateOptions(options: ExportOptions): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (options.format && !['pdf', 'png', 'svg'].includes(options.format)) {
      errors.push('Invalid format. Must be pdf, png, or svg');
    }

    if (options.quality && (options.quality < 0 || options.quality > 1)) {
      errors.push('Quality must be between 0 and 1');
    }

    if (options.scale && options.scale <= 0) {
      errors.push('Scale must be greater than 0');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }
}
