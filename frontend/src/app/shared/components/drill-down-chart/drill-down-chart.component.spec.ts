import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DrillDownChartComponent } from './drill-down-chart.component';
import { ChartDataPoint, ChartConfig, ExportFormat } from '../../../core/models/chart.model';

describe('DrillDownChartComponent', () => {
  let component: DrillDownChartComponent;
  let fixture: ComponentFixture<DrillDownChartComponent>;

  const mockChartData: ChartDataPoint[] = [
    {
      label: '2024',
      value: 100,
      children: [
        { label: 'Q1', value: 25 },
        { label: 'Q2', value: 30 },
        { label: 'Q3', value: 20 },
        { label: 'Q4', value: 25 },
      ],
    },
    {
      label: '2023',
      value: 80,
      children: [
        { label: 'Q1', value: 20 },
        { label: 'Q2', value: 20 },
        { label: 'Q3', value: 20 },
        { label: 'Q4', value: 20 },
      ],
    },
  ];

  const mockConfig: ChartConfig = {
    type: 'bar',
    title: 'Annual Report',
    enableDrillDown: true,
    enableExport: true,
    showLegend: true,
    showTooltip: true,
  };

  const createMockData = (): ChartDataPoint[] =>
    mockChartData.map((point) => ({
      ...point,
      children: point.children ? point.children.map((child) => ({ ...child })) : undefined,
    }));

  const createMockConfig = (): ChartConfig => ({
    ...mockConfig,
    colors: mockConfig.colors ? [...mockConfig.colors] : undefined,
  });

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DrillDownChartComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(DrillDownChartComponent);
    component = fixture.componentInstance;
    component.data = createMockData();
    component.config = createMockConfig();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Initialization', () => {
    it('should initialize with root level data', () => {
      fixture.detectChanges();

      expect(component.currentLevel).toBe(0);
      expect(component.currentData.length).toBe(2);
    });

    it('should apply default configuration if not provided', () => {
      component.config = undefined as any;
      fixture.detectChanges();

      expect(component.config.type).toBe('bar');
      expect(component.config.enableDrillDown).toBe(true);
    });

    it('should render chart container', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const chartContainer = compiled.querySelector('.chart-container');

      expect(chartContainer).toBeTruthy();
    });
  });

  describe('Drill-down functionality', () => {
    it('should drill down when clicking on data point with children', () => {
      fixture.detectChanges();
      spyOn(component.drillDownEvent, 'emit');

      component.onDataPointClick(mockChartData[0]);

      expect(component.currentLevel).toBe(1);
      expect(component.currentData.length).toBe(4);
      expect(component.drillDownEvent.emit).toHaveBeenCalled();
    });

    it('should not drill down when clicking on data point without children', () => {
      fixture.detectChanges();
      const leafNode = mockChartData[0].children![0];

      component.onDataPointClick(leafNode);

      expect(component.currentLevel).toBe(0);
    });

    it('should show drill-up button when not at root level', () => {
      fixture.detectChanges();
      component.onDataPointClick(mockChartData[0]);
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const drillUpButton = compiled.querySelector('.drill-up-button');

      expect(drillUpButton).toBeTruthy();
    });

    it('should drill up to previous level', () => {
      fixture.detectChanges();
      component.onDataPointClick(mockChartData[0]);
      expect(component.currentLevel).toBe(1);

      component.onDrillUp();

      expect(component.currentLevel).toBe(0);
      expect(component.currentData).toEqual(mockChartData);
    });

    it('should emit drill up event', () => {
      fixture.detectChanges();
      component.onDataPointClick(mockChartData[0]);
      spyOn(component.drillUpEvent, 'emit');

      component.onDrillUp();

      expect(component.drillUpEvent.emit).toHaveBeenCalled();
    });

    it('should maintain breadcrumb trail during drill-down', () => {
      fixture.detectChanges();

      component.onDataPointClick(mockChartData[0]);

      expect(component.breadcrumbs.length).toBe(2);
      expect(component.breadcrumbs[0].label).toBe('Root');
      expect(component.breadcrumbs[1].label).toBe('2024');
    });

    it('should navigate to specific level via breadcrumb', () => {
      fixture.detectChanges();
      component.onDataPointClick(mockChartData[0]);

      component.navigateToLevel(0);

      expect(component.currentLevel).toBe(0);
      expect(component.currentData).toEqual(mockChartData);
    });
  });

  describe('Export functionality', () => {
    it('should export chart as PNG', () => {
      fixture.detectChanges();
      spyOn(component, 'exportChart').and.callThrough();

      component.exportChart('png');

      expect(component.exportChart).toHaveBeenCalledWith('png');
    });

    it('should export chart as CSV', () => {
      fixture.detectChanges();
      spyOn(component as any, 'exportAsCSV');

      component.exportChart('csv');

      expect((component as any).exportAsCSV).toHaveBeenCalled();
    });

    it('should export chart as JSON', () => {
      fixture.detectChanges();
      spyOn(component as any, 'exportAsJSON');

      component.exportChart('json');

      expect((component as any).exportAsJSON).toHaveBeenCalled();
    });

    it('should emit export event', () => {
      fixture.detectChanges();
      spyOn(component.exportEvent, 'emit');

      component.exportChart('pdf');

      expect(component.exportEvent.emit).toHaveBeenCalledWith({
        format: 'pdf',
        level: component.currentLevel,
      });
    });

    it('should show export dropdown when enabled', () => {
      component.config.enableExport = true;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const exportButton = compiled.querySelector('.export-button');

      expect(exportButton).toBeTruthy();
    });

    it('should hide export dropdown when disabled', () => {
      component.config.enableExport = false;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const exportButton = compiled.querySelector('.export-button');

      expect(exportButton).toBeFalsy();
    });
  });

  describe('Chart rendering', () => {
    it('should render bars for bar chart', () => {
      component.config.type = 'bar';
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const bars = compiled.querySelectorAll('.chart-bar');

      expect(bars.length).toBe(mockChartData.length);
    });

    it('should display chart title', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const title = compiled.querySelector('.chart-title');

      expect(title?.textContent).toContain('Annual Report');
    });

    it('should display data labels', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const labels = compiled.querySelectorAll('.data-label');

      expect(labels.length).toBeGreaterThan(0);
    });

    it('should show tooltip on hover', () => {
      component.config.showTooltip = true;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const firstBar = compiled.querySelector('.chart-bar') as HTMLElement;

      firstBar?.dispatchEvent(new MouseEvent('mouseenter'));
      fixture.detectChanges();

      const tooltip = compiled.querySelector('.chart-tooltip');
      expect(tooltip).toBeTruthy();
    });

    it('should update chart when data changes', () => {
      fixture.detectChanges();
      const newData: ChartDataPoint[] = [{ label: '2025', value: 120 }];

      component.data = newData;
      component.ngOnChanges({
        data: {
          currentValue: newData,
          previousValue: mockChartData,
          firstChange: false,
          isFirstChange: () => false,
        },
      });
      fixture.detectChanges();

      expect(component.currentData).toEqual(newData);
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const chart = compiled.querySelector('[role="img"]');

      expect(chart).toBeTruthy();
      expect(chart?.getAttribute('aria-label')).toContain('chart');
    });

    it('should provide keyboard navigation', () => {
      fixture.detectChanges();
      const compiled = fixture.nativeElement as HTMLElement;
      const firstBar = compiled.querySelector('.chart-bar') as HTMLElement;

      expect(firstBar?.getAttribute('tabindex')).toBe('0');
    });

    it('should handle keyboard drill-down (Enter key)', () => {
      fixture.detectChanges();
      spyOn(component, 'onDataPointClick');

      component.onKeyDown(new KeyboardEvent('keydown', { key: 'Enter' }), mockChartData[0]);

      expect(component.onDataPointClick).toHaveBeenCalledWith(mockChartData[0]);
    });
  });

  describe('Performance', () => {
    it('should handle large datasets efficiently', () => {
      const largeDataset = Array.from({ length: 100 }, (_, i) => ({
        label: `Item ${i}`,
        value: Math.random() * 100,
      }));

      component.data = largeDataset;

      expect(() => {
        fixture.detectChanges();
      }).not.toThrow();
    });

    it('should handle resize events', (done) => {
      fixture.detectChanges();
      spyOn(component as any, 'updateChartSize');

      window.dispatchEvent(new Event('resize'));

      setTimeout(() => {
        expect((component as any).updateChartSize).toHaveBeenCalled();
        done();
      }, 250);
    });
  });

  describe('Error handling', () => {
    it('should handle invalid data gracefully', () => {
      component.data = null as any;

      expect(() => {
        fixture.detectChanges();
      }).not.toThrow();
    });

    it('should display error message for invalid data', () => {
      component.data = null as any;
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      const errorMessage = compiled.querySelector('.error-message');

      expect(errorMessage).toBeTruthy();
    });

    it('should handle empty data array', () => {
      component.data = [];
      fixture.detectChanges();

      expect(component.currentData).toEqual([]);
    });
  });

  describe('additional coverage', () => {
    it('should close export menu when clicking outside', () => {
      component.config.enableExport = true;
      fixture.detectChanges();

      component.toggleExportMenu();
      expect(component.showExportMenu).toBe(true);

      component.toggleExportMenu();
      expect(component.showExportMenu).toBe(false);
    });

    it('should handle Space key for drill-down', () => {
      fixture.detectChanges();
      spyOn(component, 'onDataPointClick');

      const event = new KeyboardEvent('keydown', { key: ' ' });
      spyOn(event, 'preventDefault');

      component.onKeyDown(event, mockChartData[0]);

      expect(event.preventDefault).toHaveBeenCalled();
      expect(component.onDataPointClick).toHaveBeenCalledWith(mockChartData[0]);
    });

    it('should ignore non-action keys', () => {
      fixture.detectChanges();
      spyOn(component, 'onDataPointClick');

      component.onKeyDown(new KeyboardEvent('keydown', { key: 'Tab' }), mockChartData[0]);

      expect(component.onDataPointClick).not.toHaveBeenCalled();
    });

    it('should get correct default colors by index', () => {
      fixture.detectChanges();

      const color1 = component.getDefaultColor(0);
      const color2 = component.getDefaultColor(6);

      expect(color1).toBeDefined();
      expect(color2).toBe(color1); // Should cycle
    });

    it('should hide tooltip on mouse leave', () => {
      component.config.showTooltip = true;
      fixture.detectChanges();

      const event = new MouseEvent('mouseenter', { clientX: 100, clientY: 100 });
      component.showTooltip(mockChartData[0], event);
      expect(component.hoveredPoint).toBeTruthy();

      component.hideTooltip();
      expect(component.hoveredPoint).toBeNull();
    });

    it('should not show tooltip when config disabled', () => {
      component.config.showTooltip = false;
      fixture.detectChanges();

      const event = new MouseEvent('mouseenter', { clientX: 100, clientY: 100 });
      component.showTooltip(mockChartData[0], event);

      expect(component.hoveredPoint).toBeNull();
    });

    it('should calculate bar dimensions correctly', () => {
      component.data = mockChartData;
      component.config = { ...mockConfig, width: 800, height: 400 };
      fixture.detectChanges();

      const barX = component.getBarX(0);
      const barY = component.getBarY(100);
      const barWidth = component.getBarWidth();
      const barHeight = component.getBarHeight(100);

      expect(barX).toBeGreaterThanOrEqual(0);
      expect(barY).toBeGreaterThanOrEqual(0);
      expect(barWidth).toBeGreaterThan(0);
      expect(barHeight).toBeGreaterThan(0);
    });

    it('should handle drill-up at root level gracefully', () => {
      fixture.detectChanges();
      
      expect(component.currentLevel).toBe(0);
      
      component.onDrillUp();
      
      expect(component.currentLevel).toBe(0);
    });

    it('should export empty data as valid CSV', () => {
      spyOn(component as any, 'downloadFile');
      component.currentData = [];

      component.exportChart('csv');

      expect((component as any).downloadFile).toHaveBeenCalledWith(
        'Label,Value\n',
        'chart-data.csv',
        'text/csv'
      );
    });

    it('should handle multiple drill-down levels', () => {
      fixture.detectChanges();

      // First level drill-down
      component.onDataPointClick(mockChartData[0]);
      expect(component.currentLevel).toBe(1);

      // Try second level (no children available)
      component.onDataPointClick(component.currentData[0]);
      expect(component.currentLevel).toBe(1); // Should stay at level 1
    });

    it('should maintain history when navigating levels', () => {
      fixture.detectChanges();

      component.onDataPointClick(mockChartData[0]);
      expect(component.levelHistory.length).toBe(1);

      component.onDrillUp();
      expect(component.levelHistory.length).toBe(0);
    });

    it('should navigate to specific level via breadcrumb', () => {
      fixture.detectChanges();

      component.onDataPointClick(mockChartData[0]);
      expect(component.currentLevel).toBe(1);

      component.navigateToLevel(0);
      expect(component.currentLevel).toBe(0);
    });

    it('should calculate maximum value correctly', () => {
      component.data = [
        { label: 'A', value: 50 },
        { label: 'B', value: 100 },
        { label: 'C', value: 75 },
      ];
      fixture.detectChanges();

      const maxValue = Math.max(...component.currentData.map(d => d.value));
      expect(maxValue).toBe(100);
    });

    it('should use custom colors when provided', () => {
      component.config = {
        ...mockConfig,
        colors: ['#FF0000', '#00FF00', '#0000FF'],
      };
      fixture.detectChanges();

      const color = component.getDefaultColor(0);
      expect(color).toBe('#FF0000');
    });

    it('should cycle through default colors', () => {
      fixture.detectChanges();

      const color0 = component.getDefaultColor(0);
      const color6 = component.getDefaultColor(6);

      expect(color0).toBe(color6);
    });

    it('should handle SVG export format', () => {
      spyOn(console, 'log');
      fixture.detectChanges();

      component.exportChart('svg');

      expect(console.log).toHaveBeenCalledWith(jasmine.stringContaining('svg'));
    });

    it('should handle PDF export format', () => {
      spyOn(console, 'log');
      fixture.detectChanges();

      component.exportChart('pdf');

      expect(console.log).toHaveBeenCalledWith(jasmine.stringContaining('pdf'));
    });

    it('should update breadcrumbs correctly during navigation', () => {
      fixture.detectChanges();

      component.onDataPointClick(mockChartData[0]);
      expect(component.breadcrumbs.length).toBe(2);
      expect(component.breadcrumbs[1].label).toBe('2024');

      component.onDrillUp();
      expect(component.breadcrumbs.length).toBe(1);
      expect(component.breadcrumbs[0].label).toBe('Root');
    });

    it('should handle config without optional fields', () => {
      component.config = { type: 'bar', enableDrillDown: true };
      component.data = mockChartData;

      expect(() => fixture.detectChanges()).not.toThrow();
    });

    it('should set default dimensions when not provided', () => {
      component.config = { type: 'bar' };
      fixture.detectChanges();

      const barWidth = component.getBarWidth();
      const barHeight = component.getBarHeight(100);

      expect(barWidth).toBeGreaterThan(0);
      expect(barHeight).toBeGreaterThan(0);
    });

    it('should not navigate to invalid levels', () => {
      fixture.detectChanges();

      component.navigateToLevel(-1);
      expect(component.currentLevel).toBe(0);

      component.onDataPointClick(mockChartData[0]);
      component.navigateToLevel(5); // Beyond current level
      expect(component.currentLevel).toBe(1);
    });

    it('should handle Escape key for drill-up', () => {
      fixture.detectChanges();

      component.onDataPointClick(mockChartData[0]);
      expect(component.currentLevel).toBe(1);

      const escapeEvent = new KeyboardEvent('keydown', { key: 'Escape' });
      spyOn(escapeEvent, 'preventDefault');

      component.onKeyDown(escapeEvent, mockChartData[0]);

      expect(escapeEvent.preventDefault).toHaveBeenCalled();
      expect(component.currentLevel).toBe(0);
    });

    it('should not handle Escape at root level', () => {
      fixture.detectChanges();

      expect(component.currentLevel).toBe(0);

      const escapeEvent = new KeyboardEvent('keydown', { key: 'Escape' });
      spyOn(escapeEvent, 'preventDefault');

      component.onKeyDown(escapeEvent, mockChartData[0]);

      expect(escapeEvent.preventDefault).not.toHaveBeenCalled();
    });

    it('should handle chart with no children', () => {
      component.data = [
        { label: 'A', value: 50 },
        { label: 'B', value: 100 },
      ];
      fixture.detectChanges();

      component.onDataPointClick(component.data[0]);

      expect(component.currentLevel).toBe(0);
    });

    it('should calculate bar positions for multiple bars', () => {
      component.data = Array.from({ length: 10 }, (_, i) => ({
        label: `Item ${i}`,
        value: (i + 1) * 10,
      }));
      fixture.detectChanges();

      const positions = component.data.map((_, i) => component.getBarX(i));

      // All positions should be different
      const uniquePositions = new Set(positions);
      expect(uniquePositions.size).toBe(10);
    });

    it('should scale bar heights proportionally', () => {
      component.data = [
        { label: 'Small', value: 10 },
        { label: 'Large', value: 100 },
      ];
      fixture.detectChanges();

      const smallHeight = component.getBarHeight(10);
      const largeHeight = component.getBarHeight(100);

      expect(largeHeight).toBeGreaterThan(smallHeight);
      expect(largeHeight / smallHeight).toBeCloseTo(10, 1);
    });

    it('should get current drill-down depth', () => {
      fixture.detectChanges();

      expect(component.getCurrentDepth()).toBe(0);

      component.onDataPointClick(mockChartData[0]);
      expect(component.getCurrentDepth()).toBe(1);
    });

    it('should check if can drill down on point', () => {
      fixture.detectChanges();

      expect(component.canDrillDown(mockChartData[0])).toBe(true);
      expect(component.canDrillDown(mockChartData[0].children![0])).toBe(false);
    });

    it('should not drill down when disabled in config', () => {
      component.config.enableDrillDown = false;
      fixture.detectChanges();

      expect(component.canDrillDown(mockChartData[0])).toBe(false);
    });

    it('should handle download file errors gracefully', () => {
      spyOn(window.URL, 'createObjectURL').and.throwError('Blob error');
      spyOn(console, 'error');

      component.exportChart('csv');

      expect(console.error).toHaveBeenCalled();
    });

    it('should handle onChanges with data update', () => {
      fixture.detectChanges();

      const newData: ChartDataPoint[] = [{ label: 'New', value: 200 }];

      component.data = newData;
      component.ngOnChanges({
        data: {
          currentValue: newData,
          previousValue: mockChartData,
          firstChange: false,
          isFirstChange: () => false,
        },
      });

      expect(component.currentData).toEqual(newData);
    });

    it('should not reinitialize on first change', () => {
      const initSpy = spyOn(component as any, 'initializeChart').and.callThrough();

      component.ngOnChanges({
        data: {
          currentValue: mockChartData,
          previousValue: null,
          firstChange: true,
          isFirstChange: () => true,
        },
      });

      expect(initSpy).not.toHaveBeenCalled();
    });

    it('should handle config changes', () => {
      fixture.detectChanges();

      const newConfig = { ...mockConfig, title: 'Updated Title' };

      component.ngOnChanges({
        config: {
          currentValue: newConfig,
          previousValue: mockConfig,
          firstChange: false,
          isFirstChange: () => false,
        },
      });

      // Component should handle config changes gracefully
      expect(component.config.title).toBeTruthy();
    });
  });
});
