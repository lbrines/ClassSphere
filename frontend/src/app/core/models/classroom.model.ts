export type IntegrationMode = 'mock' | 'google';

export interface SummaryMetric {
  id: string;
  label: string;
  value: number;
  delta: number;
  trend: 'up' | 'down' | 'flat';
  format?: 'percent' | 'number';
}

export interface ChartPoint {
  x: string | number;
  y: number;
}

export interface ChartSeries {
  name: string;
  data: ChartPoint[];
}

export interface ChartData {
  id: string;
  title: string;
  type: 'area' | 'bar' | 'line' | 'donut';
  series: ChartSeries[];
  categories?: string[];
}

export interface Highlight {
  id: string;
  title: string;
  details: string;
  status: 'info' | 'warning' | 'success';
}

export interface CourseOverview {
  id: string;
  name: string;
  section: string;
  program: string;
  primaryTeacher: string;
  enrollment: number;
  completionRate: number;
  upcomingAssignments: number;
  lastActivity: string;
}

export interface TimelineItem {
  id: string;
  title: string;
  dueDate: string;
  courseId: string;
  status: 'onTrack' | 'pending' | 'atRisk';
}

export interface DashboardData {
  role: string;
  mode: IntegrationMode;
  generatedAt: string;
  summary: SummaryMetric[];
  charts: ChartData[];
  highlights: Highlight[];
  courses?: CourseOverview[];
  timeline?: TimelineItem[];
  alerts?: string[];
}

export interface CourseListResponse {
  mode: IntegrationMode;
  generatedAt: string;
  courses: CourseOverview[];
  availableModes: IntegrationMode[];
}
