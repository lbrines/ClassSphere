import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChartComponent } from './chart.component';

describe('ChartComponent', () => {
  let component: ChartComponent;
  let fixture: ComponentFixture<ChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ChartComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with default values', () => {
    expect(component.type).toBe('bar');
    expect(component.title).toBe('Chart');
    expect(component.showDrillDown).toBe(false);
    expect(component.data).toEqual([]);
  });

  it('should process data correctly for bar chart', (done) => {
    component.data = [
      { id: 1, label: 'Test 1', value: 10 },
      { id: 2, label: 'Test 2', value: 20 },
      { id: 3, label: 'Test 3', value: 30 }
    ];
    component.type = 'bar';
    
    component.ngOnInit();
    
    // Wait for async processing
    setTimeout(() => {
      expect(component.chartData()).toBeTruthy();
      expect(component.chartData()?.labels).toEqual(['Test 1', 'Test 2', 'Test 3']);
      expect(component.chartData()?.datasets[0].data).toEqual([10, 20, 30]);
      done();
    }, 400);
  });

  it('should process data correctly for pie chart', (done) => {
    component.data = [
      { id: 1, label: 'Category A', value: 40 },
      { id: 2, label: 'Category B', value: 60 }
    ];
    component.type = 'pie';
    
    component.ngOnInit();
    
    // Wait for async processing
    setTimeout(() => {
      expect(component.chartData()).toBeTruthy();
      expect(component.chartData()?.labels).toEqual(['Category A', 'Category B']);
      expect(component.chartData()?.datasets[0].data).toEqual([40, 60]);
      done();
    }, 400);
  });

  it('should calculate statistics correctly', () => {
    component.data = [
      { id: 1, value: 10 },
      { id: 2, value: 20 },
      { id: 3, value: 30 }
    ];
    
    component.ngOnInit();
    
    const stats = component.chartStats();
    expect(stats.length).toBe(4);
    expect(stats[0].value).toBe('60'); // Total
    expect(stats[1].value).toBe('20.0'); // Average
    expect(stats[2].value).toBe('30'); // Max
    expect(stats[3].value).toBe('10'); // Min
  });

  it('should toggle chart type correctly', () => {
    component.type = 'bar';
    component.ngOnInit();
    
    expect(component.currentChartType()).toBe('bar');
    
    component.toggleChartType();
    expect(component.currentChartType()).toBe('line');
    
    component.toggleChartType();
    expect(component.currentChartType()).toBe('pie');
    
    component.toggleChartType();
    expect(component.currentChartType()).toBe('doughnut');
    
    component.toggleChartType();
    expect(component.currentChartType()).toBe('bar');
  });

  it('should handle empty data gracefully', () => {
    component.data = [];
    component.ngOnInit();
    
    expect(component.chartData()).toBeNull();
    expect(component.chartStats()).toEqual([]);
  });

  it('should handle drill down functionality', () => {
    component.showDrillDown = true;
    component.drillDownCallback = (data: any) => [
      { detail: 'Detail 1', value: 100 },
      { detail: 'Detail 2', value: 200 }
    ];
    
    const mockEvent = {
      data: { label: 'Test Item', value: 50 }
    };
    
    component.onChartClick(mockEvent);
    
    expect(component.drillDownData().length).toBe(2);
    expect(component.drillDownTitle()).toBe('Details for Test Item');
  });

  it('should reset drill down data', () => {
    component.drillDownData.set([
      { detail: 'Detail 1', value: 100 }
    ]);
    component.drillDownTitle.set('Test Title');
    
    component.resetDrillDown();
    
    expect(component.drillDownData()).toEqual([]);
    expect(component.drillDownTitle()).toBe('');
  });

  it('should generate correct chart type labels', () => {
    component.type = 'bar';
    component.ngOnInit();
    
    expect(component.getChartTypeLabel()).toBe('Switch to Line');
    
    component.currentChartType.set('line');
    expect(component.getChartTypeLabel()).toBe('Switch to Pie');
    
    component.currentChartType.set('pie');
    expect(component.getChartTypeLabel()).toBe('Switch to Doughnut');
    
    component.currentChartType.set('doughnut');
    expect(component.getChartTypeLabel()).toBe('Switch to Bar');
  });

  it('should handle data changes', (done) => {
    component.data = [{ id: 1, value: 10 }];
    component.ngOnInit();
    
    component.data = [{ id: 1, value: 10 }, { id: 2, value: 20 }];
    component.ngOnChanges({
      data: {
        currentValue: component.data,
        previousValue: [{ id: 1, value: 10 }],
        firstChange: false,
        isFirstChange: () => false
      }
    });
    
    // Wait for async processing
    setTimeout(() => {
      // Data should be reprocessed
      expect(component.chartData()).toBeTruthy();
      done();
    }, 400);
  });

  it('should generate colors correctly', () => {
    const colors = component['generateColors'](3, 0.7);
    expect(colors.length).toBe(3);
    expect(colors[0]).toContain('rgba(59, 130, 246, 0.7)');
    expect(colors[1]).toContain('rgba(16, 185, 129, 0.7)');
    expect(colors[2]).toContain('rgba(245, 101, 101, 0.7)');
  });

  it('should get dataset color correctly', () => {
    const dataset = {
      label: 'Test',
      data: [1, 2, 3],
      backgroundColor: ['#FF0000', '#00FF00', '#0000FF']
    };
    
    expect(component.getDatasetColor(dataset, 0)).toBe('#FF0000');
    expect(component.getDatasetColor(dataset, 1)).toBe('#00FF00');
    expect(component.getDatasetColor(dataset, 2)).toBe('#0000FF');
  });

  it('should handle single color background', () => {
    const dataset = {
      label: 'Test',
      data: [1, 2, 3],
      backgroundColor: '#FF0000'
    };
    
    expect(component.getDatasetColor(dataset, 0)).toBe('#FF0000');
    expect(component.getDatasetColor(dataset, 1)).toBe('#FF0000');
  });

  it('should get drill down headers correctly', () => {
    component.drillDownData.set([
      { name: 'Item 1', value: 100, category: 'A' },
      { name: 'Item 2', value: 200, category: 'B' }
    ]);
    
    const headers = component.drillDownHeaders();
    expect(headers).toEqual(['name', 'value', 'category']);
  });

  it('should return empty headers for empty drill down data', () => {
    component.drillDownData.set([]);
    
    const headers = component.drillDownHeaders();
    expect(headers).toEqual([]);
  });
});
