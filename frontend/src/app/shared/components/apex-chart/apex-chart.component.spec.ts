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
});
