/**
 * Chart Models for Phase 3 - Interactive Drill-down Charts
 * Supports hierarchical data visualization with drill-down capability
 */

export type ChartType = 'bar' | 'line' | 'pie' | 'donut' | 'area';
export type ExportFormat = 'pdf' | 'png' | 'svg' | 'csv' | 'json';

export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
  metadata?: Record<string, any>;
  children?: ChartDataPoint[]; // For drill-down
}

export interface ChartSeries {
  name: string;
  data: ChartDataPoint[];
  type?: ChartType;
  color?: string;
}

export interface ChartConfig {
  type: ChartType;
  title?: string;
  subtitle?: string;
  xAxisLabel?: string;
  yAxisLabel?: string;
  showLegend?: boolean;
  showTooltip?: boolean;
  enableDrillDown?: boolean;
  enableExport?: boolean;
  height?: number;
  width?: number;
  colors?: string[];
}

export interface DrillDownLevel {
  level: number;
  title: string;
  data: ChartSeries[];
  parent?: ChartDataPoint;
}

export interface ChartState {
  currentLevel: number;
  levels: DrillDownLevel[];
  loading: boolean;
  error: string | null;
}

export interface ExportOptions {
  format: ExportFormat;
  filename: string;
  includeData?: boolean;
  quality?: number; // For PNG/JPG (0-1)
}

export interface ChartInteractionEvent {
  type: 'click' | 'hover' | 'drill-down' | 'drill-up' | 'export';
  dataPoint?: ChartDataPoint;
  level?: number;
  timestamp: number;
}

