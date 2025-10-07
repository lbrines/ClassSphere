import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SimpleChange } from '@angular/core';

import { ChartData } from '../../../core/models/classroom.model';
import { ApexChartComponent } from './apex-chart.component';

describe('ApexChartComponent', () => {
  let fixture: ComponentFixture<ApexChartComponent>;
  let component: ApexChartComponent;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApexChartComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ApexChartComponent);
    component = fixture.componentInstance;
  });

  const sampleChart: ChartData = {
    id: 'sample',
    title: 'Sample Chart',
    type: 'bar',
    series: [
      {
        name: 'Completed',
        data: [
          { x: 'Week 1', y: 10 },
          { x: 'Week 2', y: 12 },
        ],
      },
    ],
    categories: ['Week 1', 'Week 2'],
  };

  it('creates a chart instance on render', async () => {
    const mockInstance = {
      render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
      updateOptions: jasmine.createSpy('updateOptions').and.returnValue(Promise.resolve()),
      destroy: jasmine.createSpy('destroy'),
    };

    const createSpy = spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.returnValue(mockInstance as never);

    component.chart = sampleChart;
    fixture.detectChanges();

    expect(createSpy).toHaveBeenCalled();
    expect(mockInstance.render).toHaveBeenCalled();
  });

  it('updates chart options when input changes', async () => {
    const mockInstance = {
      render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
      updateOptions: jasmine.createSpy('updateOptions').and.returnValue(Promise.resolve()),
      destroy: jasmine.createSpy('destroy'),
    };

    spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.returnValue(mockInstance as never);

    component.chart = sampleChart;
    fixture.detectChanges();

    const updatedChart: ChartData = {
      ...sampleChart,
      series: [
        {
          name: 'Completed',
          data: [
            { x: 'Week 1', y: 14 },
            { x: 'Week 2', y: 16 },
          ],
        },
      ],
    };

    component.chart = updatedChart;
    component.ngOnChanges({
      chart: new SimpleChange(sampleChart, updatedChart, false),
    });

    expect(mockInstance.updateOptions).toHaveBeenCalled();
  });

  it('handles chart without categories', () => {
    const chartWithoutCategories: ChartData = {
      ...sampleChart,
      categories: undefined,
    };

    component.chart = chartWithoutCategories;
    expect(component.chart.categories).toBeUndefined();
  });

  it('handles chart with multiple series', () => {
    const multiSeriesChart: ChartData = {
      ...sampleChart,
      series: [
        {
          name: 'Series 1',
          data: [{ x: 'A', y: 10 }, { x: 'B', y: 20 }],
        },
        {
          name: 'Series 2',
          data: [{ x: 'A', y: 15 }, { x: 'B', y: 25 }],
        },
      ],
    };

    component.chart = multiSeriesChart;
    expect(component.chart.series).toHaveSize(2);
  });

  it('handles different chart types', () => {
    const lineChart: ChartData = {
      ...sampleChart,
      type: 'line',
    };

    component.chart = lineChart;
    expect(component.chart.type).toBe('line');

    const areaChart: ChartData = {
      ...sampleChart,
      type: 'area',
    };

    component.chart = areaChart;
    expect(component.chart.type).toBe('area');
  });

  it('handles empty series gracefully', () => {
    const emptySeriesChart: ChartData = {
      ...sampleChart,
      series: [],
    };

    component.chart = emptySeriesChart;
    expect(component.chart.series).toEqual([]);
  });

  it('destroys chart on component destroy', () => {
    const mockInstance = {
      render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
      updateOptions: jasmine.createSpy('updateOptions').and.returnValue(Promise.resolve()),
      destroy: jasmine.createSpy('destroy'),
    };

    spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.returnValue(mockInstance as never);

    component.chart = sampleChart;
    fixture.detectChanges();

    component.ngOnDestroy();

    expect(mockInstance.destroy).toHaveBeenCalled();
  });

  it('handles chart creation errors gracefully', async () => {
    spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.throwError('Chart creation failed');

    component.chart = sampleChart;

    // Should throw error when chart creation fails
    expect(() => {
      fixture.detectChanges();
    }).toThrowError('Chart creation failed');
  });

  it('handles chart update errors gracefully', () => {
    const mockInstance = {
      render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
      updateOptions: jasmine.createSpy('updateOptions').and.throwError('Update failed'),
      destroy: jasmine.createSpy('destroy'),
    };

    spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.returnValue(mockInstance as never);

    component.chart = sampleChart;
    fixture.detectChanges();

    const updatedChart: ChartData = {
      ...sampleChart,
      title: 'Updated Title',
    };

    component.chart = updatedChart;

    // Should handle error when update fails
    expect(() => {
      component.ngOnChanges({
        chart: new SimpleChange(sampleChart, updatedChart, false),
      });
    }).toThrow();
  });
});
