import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SimpleChange } from '@angular/core';
import { ApexOptions } from 'apexcharts';

import { ChartData } from '../../../core/models/classroom.model';
import { ApexChartComponent } from './apex-chart.component';

describe('ApexChartComponent', () => {
  let fixture: ComponentFixture<ApexChartComponent>;
  let component: ApexChartComponent;

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

  const createMockInstance = () => ({
    render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
    updateOptions: jasmine.createSpy('updateOptions').and.returnValue(Promise.resolve()),
    destroy: jasmine.createSpy('destroy'),
  });

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApexChartComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ApexChartComponent);
    component = fixture.componentInstance;
  });

  function renderWith(chart: ChartData) {
    const mockInstance = createMockInstance();
    let capturedOptions: ApexOptions | undefined;

    const createSpy = spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.callFake(
      (_element: HTMLElement, options: ApexOptions) => {
        capturedOptions = options;
        return mockInstance as never;
      },
    );

    component.chart = chart;
    fixture.detectChanges();

    return { mockInstance, createSpy, capturedOptions };
  }

  it('creates a chart instance with standard options on render', () => {
    const { mockInstance, createSpy, capturedOptions } = renderWith(sampleChart);

    expect(createSpy).toHaveBeenCalled();
    expect(mockInstance.render).toHaveBeenCalled();
    expect(capturedOptions?.xaxis).toEqual(
      jasmine.objectContaining({
        categories: ['Week 1', 'Week 2'],
      }),
    );
  });

  it('updates chart options when input changes', () => {
    const { mockInstance } = renderWith(sampleChart);

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

    expect(mockInstance.updateOptions).toHaveBeenCalledWith(jasmine.any(Object), true, true);
  });

  it('skips render when chart input is missing', () => {
    const createSpy = spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart');
    fixture.detectChanges();

    expect(createSpy).not.toHaveBeenCalled();
  });

  it('skips update when no chart instance exists yet', () => {
    const buildOptionsSpy = spyOn(component as any, 'buildOptions').and.callThrough();

    component.chart = sampleChart;
    component.ngOnChanges({
      chart: new SimpleChange(sampleChart, sampleChart, false),
    });

    expect(buildOptionsSpy).not.toHaveBeenCalled();
  });

  it('builds donut chart options with aggregated labels and series', () => {
    const donutChart: ChartData = {
      ...sampleChart,
      type: 'donut',
      series: [
        {
          name: 'Status',
          data: [
            { x: 'Completed', y: 30 },
            { x: 'Pending', y: 70 },
          ],
        },
      ],
      categories: undefined,
    };

    const { capturedOptions } = renderWith(donutChart);

    expect(capturedOptions?.chart?.type).toBe('donut');
    expect(capturedOptions?.labels).toEqual(['Completed', 'Pending']);
    expect(capturedOptions?.series).toEqual([30, 70]);
  });

  it('builds fallback x-axis config when categories are missing', () => {
    const chartWithoutCategories: ChartData = {
      ...sampleChart,
      categories: undefined,
    };

    const { capturedOptions } = renderWith(chartWithoutCategories);

    expect(capturedOptions?.xaxis).toEqual(
      jasmine.objectContaining({
        labels: jasmine.objectContaining({
          style: jasmine.objectContaining({ colors: '#cbd5f5' }),
        }),
      }),
    );
    expect((capturedOptions?.xaxis as { categories?: unknown }).categories).toBeUndefined();
  });

  it('uses gradient fill and smooth stroke for area charts', () => {
    const areaChart: ChartData = {
      ...sampleChart,
      type: 'area',
    };

    const { capturedOptions } = renderWith(areaChart);

    expect(capturedOptions?.stroke).toEqual(jasmine.objectContaining({ curve: 'smooth' }));
    expect(capturedOptions?.fill).toEqual(jasmine.objectContaining({ type: 'gradient' }));
  });

  it('destroys the chart instance on component destroy', () => {
    const { mockInstance } = renderWith(sampleChart);

    component.ngOnDestroy();

    expect(mockInstance.destroy).toHaveBeenCalled();
  });

  it('propagates chart creation errors', () => {
    spyOn(component as unknown as { createChart: typeof component['createChart'] }, 'createChart').and.throwError('Chart creation failed');

    component.chart = sampleChart;

    expect(() => fixture.detectChanges()).toThrowError('Chart creation failed');
  });

  it('propagates chart update errors', () => {
    const mockInstance = {
      render: jasmine.createSpy('render').and.returnValue(Promise.resolve()),
      updateOptions: jasmine.createSpy('updateOptions').and.callFake(() => {
        throw new Error('Update failed');
      }),
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

    expect(() =>
      component.ngOnChanges({
        chart: new SimpleChange(sampleChart, updatedChart, false),
      }),
    ).toThrowError('Update failed');
  });
});
