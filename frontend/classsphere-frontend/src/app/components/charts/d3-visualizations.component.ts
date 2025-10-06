import { Component, OnInit, signal, computed, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import * as d3 from 'd3';

interface D3DataPoint {
  id: string;
  name: string;
  value: number;
  category: string;
  x?: number;
  y?: number;
  children?: D3DataPoint[];
}

@Component({
  selector: 'app-d3-visualizations',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="px-4 py-6 sm:px-0">
      <!-- Page Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Visualizaciones D3.js</h1>
        <p class="mt-2 text-gray-600">
          Visualizaciones custom con D3.js para análisis avanzado de datos
        </p>
      </div>

      <!-- Visualization Controls -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Controles de Visualización</h3>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Visualización</label>
              <select
                [(ngModel)]="selectedVisualization"
                (change)="updateVisualization()"
                class="w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="force-directed">Grafo de Fuerza</option>
                <option value="treemap">Treemap</option>
                <option value="sankey">Diagrama Sankey</option>
                <option value="heatmap">Mapa de Calor</option>
                <option value="network">Red de Conexiones</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Datos</label>
              <select
                [(ngModel)]="selectedDataset"
                (change)="updateVisualization()"
                class="w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="courses">Cursos y Estudiantes</option>
                <option value="assignments">Tareas y Calificaciones</option>
                <option value="performance">Rendimiento</option>
                <option value="network">Red Social</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Animación</label>
              <div class="flex items-center space-x-2">
                <input
                  type="checkbox"
                  [(ngModel)]="enableAnimation"
                  (change)="updateVisualization()"
                  class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                >
                <span class="text-sm text-gray-700">Habilitar</span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Acciones</label>
              <div class="flex space-x-2">
                <button
                  (click)="exportVisualization()"
                  class="px-3 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700"
                >
                  Exportar SVG
                </button>
                <button
                  (click)="resetVisualization()"
                  class="px-3 py-2 bg-gray-600 text-white text-sm rounded-md hover:bg-gray-700"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Visualization Container -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">
              {{ getVisualizationTitle() }}
            </h3>
            <div class="text-sm text-gray-500">
              {{ getDataInfo() }}
            </div>
          </div>
          
          <!-- D3 Visualization Container -->
          <div 
            #visualizationContainer
            class="w-full border border-gray-200 rounded-lg"
            [style.height.px]="visualizationHeight"
          ></div>
        </div>
      </div>

      <!-- Visualization Details -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Data Summary -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Resumen de Datos</h3>
            <div class="space-y-3">
              @for (stat of getDataSummary(); track stat.label) {
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">{{ stat.label }}</span>
                  <span class="text-sm font-medium text-gray-900">{{ stat.value }}</span>
                </div>
              }
            </div>
          </div>
        </div>

        <!-- Interaction Info -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Información de Interacción</h3>
            <div class="space-y-3">
              <div class="text-sm text-gray-600">
                <strong>Hover:</strong> Muestra detalles del elemento
              </div>
              <div class="text-sm text-gray-600">
                <strong>Click:</strong> Selecciona elemento
              </div>
              <div class="text-sm text-gray-600">
                <strong>Drag:</strong> Mueve elementos (si aplica)
              </div>
              <div class="text-sm text-gray-600">
                <strong>Zoom:</strong> Rueda del mouse para zoom
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class D3VisualizationsComponent implements OnInit, AfterViewInit {
  @ViewChild('visualizationContainer', { static: false }) 
  visualizationContainer!: ElementRef;

  selectedVisualization = signal<string>('force-directed');
  selectedDataset = signal<string>('courses');
  enableAnimation = signal<boolean>(true);
  visualizationHeight = 500;

  private svg: any;
  private width = 800;
  private height = 500;
  private data: D3DataPoint[] = [];

  constructor() {}

  ngOnInit(): void {
    this.updateVisualization();
  }

  ngAfterViewInit(): void {
    this.updateVisualization();
  }

  updateVisualization(): void {
    if (!this.visualizationContainer) return;

    // Clear previous visualization
    d3.select(this.visualizationContainer.nativeElement).selectAll('*').remove();

    // Set up SVG
    this.svg = d3.select(this.visualizationContainer.nativeElement)
      .append('svg')
      .attr('width', '100%')
      .attr('height', this.visualizationHeight)
      .attr('viewBox', `0 0 ${this.width} ${this.height}`)
      .style('background-color', '#f9fafb');

    // Load data and create visualization
    this.loadData();
    this.createVisualization();
  }

  loadData(): void {
    const dataset = this.selectedDataset();
    
    switch (dataset) {
      case 'courses':
        this.data = this.generateCourseData();
        break;
      case 'assignments':
        this.data = this.generateAssignmentData();
        break;
      case 'performance':
        this.data = this.generatePerformanceData();
        break;
      case 'network':
        this.data = this.generateNetworkData();
        break;
      default:
        this.data = this.generateCourseData();
    }
  }

  createVisualization(): void {
    const visualizationType = this.selectedVisualization();
    
    switch (visualizationType) {
      case 'force-directed':
        this.createForceDirectedGraph();
        break;
      case 'treemap':
        this.createTreemap();
        break;
      case 'sankey':
        this.createSankeyDiagram();
        break;
      case 'heatmap':
        this.createHeatmap();
        break;
      case 'network':
        this.createNetworkGraph();
        break;
      default:
        this.createForceDirectedGraph();
    }
  }

  createForceDirectedGraph(): void {
    const data = this.data;
    
    // Create force simulation
    const simulation = d3.forceSimulation(data)
      .force('link', d3.forceLink().id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2));

    // Create links
    const links = this.svg.append('g')
      .selectAll('line')
      .data(this.generateLinks(data))
      .enter().append('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 2);

    // Create nodes
    const nodes = this.svg.append('g')
      .selectAll('circle')
      .data(data)
      .enter().append('circle')
      .attr('r', (d: D3DataPoint) => Math.sqrt(d.value) * 2 + 5)
      .attr('fill', (d: D3DataPoint) => this.getColorForCategory(d.category))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .call(this.drag(simulation) as any);

    // Add labels
    const labels = this.svg.append('g')
      .selectAll('text')
      .data(data)
      .enter().append('text')
      .text((d: D3DataPoint) => d.name)
      .attr('font-size', '12px')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', '#333');

    // Add tooltips
    nodes.append('title')
      .text((d: D3DataPoint) => `${d.name}\nValor: ${d.value}\nCategoría: ${d.category}`);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      links
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      nodes
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      labels
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);
    });
  }

  createTreemap(): void {
    const data = this.data;
    
    // Create treemap layout
    const treemap = d3.treemap()
      .size([this.width, this.height])
      .padding(2);

    const root = d3.hierarchy({ children: data })
      .sum((d: any) => d.value);

    treemap(root as any);

    // Create cells
    const cells = this.svg.selectAll('g')
      .data(root.leaves())
      .enter().append('g')
      .attr('transform', (d: any) => `translate(${d.x0},${d.y0})`);

    cells.append('rect')
      .attr('width', (d: any) => d.x1 - d.x0)
      .attr('height', (d: any) => d.y1 - d.y0)
      .attr('fill', (d: any) => this.getColorForCategory(d.data.category))
      .attr('stroke', '#fff')
      .attr('stroke-width', 1);

    cells.append('text')
      .attr('x', (d: any) => (d.x1 - d.x0) / 2)
      .attr('y', (d: any) => (d.y1 - d.y0) / 2)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#333')
      .text((d: any) => d.data.name)
      .call(this.wrap, 100);
  }

  createSankeyDiagram(): void {
    // Simplified Sankey diagram
    const data = this.data;
    const levels = 3;
    const levelWidth = this.width / levels;
    
    // Position nodes
    data.forEach((d, i) => {
      const level = i % levels;
      d.x = level * levelWidth + levelWidth / 2;
      d.y = (i / levels) * (this.height / Math.ceil(data.length / levels)) + 50;
    });

    // Create nodes
    const nodes = this.svg.selectAll('circle')
      .data(data)
      .enter().append('circle')
      .attr('cx', (d: D3DataPoint) => d.x!)
      .attr('cy', (d: D3DataPoint) => d.y!)
      .attr('r', (d: D3DataPoint) => Math.sqrt(d.value) * 2 + 5)
      .attr('fill', (d: D3DataPoint) => this.getColorForCategory(d.category))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2);

    // Create flows (simplified)
    for (let i = 0; i < data.length - 1; i++) {
      const source = data[i];
      const target = data[i + 1];
      
      this.svg.append('path')
        .datum({ source, target })
        .attr('d', this.createFlowPath(source, target))
        .attr('fill', 'none')
        .attr('stroke', '#999')
        .attr('stroke-width', 2)
        .attr('stroke-opacity', 0.6);
    }

    // Add labels
    this.svg.selectAll('text')
      .data(data)
      .enter().append('text')
      .attr('x', (d: D3DataPoint) => d.x!)
      .attr('y', (d: D3DataPoint) => d.y! + 20)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#333')
      .text((d: D3DataPoint) => d.name);
  }

  createHeatmap(): void {
    const data = this.data;
    const cellSize = 50;
    const cols = Math.ceil(Math.sqrt(data.length));
    const rows = Math.ceil(data.length / cols);

    // Create heatmap cells
    const cells = this.svg.selectAll('rect')
      .data(data)
      .enter().append('rect')
      .attr('x', (d: D3DataPoint, i: number) => (i % cols) * cellSize)
      .attr('y', (d: D3DataPoint, i: number) => Math.floor(i / cols) * cellSize)
      .attr('width', cellSize)
      .attr('height', cellSize)
      .attr('fill', (d: D3DataPoint) => this.getHeatmapColor(d.value))
      .attr('stroke', '#fff')
      .attr('stroke-width', 1);

    // Add labels
    this.svg.selectAll('text')
      .data(data)
      .enter().append('text')
      .attr('x', (d: D3DataPoint, i: number) => (i % cols) * cellSize + cellSize / 2)
      .attr('y', (d: D3DataPoint, i: number) => Math.floor(i / cols) * cellSize + cellSize / 2)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('font-size', '10px')
      .attr('fill', '#333')
      .text((d: D3DataPoint) => d.name.substring(0, 8));
  }

  createNetworkGraph(): void {
    // Similar to force-directed but with different styling
    this.createForceDirectedGraph();
  }

  // Helper methods
  generateCourseData(): D3DataPoint[] {
    return [
      { id: 'math101', name: 'Matemáticas 101', value: 25, category: 'course' },
      { id: 'physics201', name: 'Física 201', value: 18, category: 'course' },
      { id: 'algebra', name: 'Álgebra Lineal', value: 22, category: 'course' },
      { id: 'student1', name: 'Juan Pérez', value: 15, category: 'student' },
      { id: 'student2', name: 'María García', value: 12, category: 'student' },
      { id: 'student3', name: 'Carlos López', value: 20, category: 'student' },
      { id: 'teacher1', name: 'Dr. García', value: 8, category: 'teacher' },
      { id: 'teacher2', name: 'Prof. López', value: 6, category: 'teacher' }
    ];
  }

  generateAssignmentData(): D3DataPoint[] {
    return [
      { id: 'hw1', name: 'Tarea 1', value: 30, category: 'assignment' },
      { id: 'hw2', name: 'Tarea 2', value: 25, category: 'assignment' },
      { id: 'exam1', name: 'Examen 1', value: 40, category: 'exam' },
      { id: 'project1', name: 'Proyecto 1', value: 35, category: 'project' },
      { id: 'grade_a', name: 'Calificación A', value: 20, category: 'grade' },
      { id: 'grade_b', name: 'Calificación B', value: 30, category: 'grade' },
      { id: 'grade_c', name: 'Calificación C', value: 15, category: 'grade' }
    ];
  }

  generatePerformanceData(): D3DataPoint[] {
    return [
      { id: 'excellent', name: 'Excelente', value: 20, category: 'performance' },
      { id: 'good', name: 'Bueno', value: 35, category: 'performance' },
      { id: 'average', name: 'Regular', value: 30, category: 'performance' },
      { id: 'poor', name: 'Necesita Mejora', value: 12, category: 'performance' },
      { id: 'critical', name: 'Crítico', value: 3, category: 'performance' }
    ];
  }

  generateNetworkData(): D3DataPoint[] {
    return [
      { id: 'node1', name: 'Nodo 1', value: 25, category: 'node' },
      { id: 'node2', name: 'Nodo 2', value: 18, category: 'node' },
      { id: 'node3', name: 'Nodo 3', value: 22, category: 'node' },
      { id: 'node4', name: 'Nodo 4', value: 15, category: 'node' },
      { id: 'node5', name: 'Nodo 5', value: 12, category: 'node' },
      { id: 'node6', name: 'Nodo 6', value: 20, category: 'node' }
    ];
  }

  generateLinks(data: D3DataPoint[]): any[] {
    const links = [];
    for (let i = 0; i < data.length - 1; i++) {
      if (Math.random() > 0.5) {
        links.push({ source: data[i], target: data[i + 1] });
      }
    }
    return links;
  }

  getColorForCategory(category: string): string {
    const colors: { [key: string]: string } = {
      course: '#3B82F6',
      student: '#10B981',
      teacher: '#F59E0B',
      assignment: '#EF4444',
      exam: '#8B5CF6',
      project: '#06B6D4',
      grade: '#84CC16',
      performance: '#F97316',
      node: '#6B7280'
    };
    return colors[category] || '#6B7280';
  }

  getHeatmapColor(value: number): string {
    const max = Math.max(...this.data.map(d => d.value));
    const intensity = value / max;
    return d3.interpolateBlues(intensity);
  }

  createFlowPath(source: D3DataPoint, target: D3DataPoint): string {
    const x1 = source.x!;
    const y1 = source.y!;
    const x2 = target.x!;
    const y2 = target.y!;
    
    const midX = (x1 + x2) / 2;
    
    return `M ${x1} ${y1} Q ${midX} ${y1} ${midX} ${(y1 + y2) / 2} Q ${midX} ${y2} ${x2} ${y2}`;
  }

  drag(simulation: any) {
    return d3.drag()
      .on('start', (event: any, d: any) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on('drag', (event: any, d: any) => {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on('end', (event: any, d: any) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      });
  }

  wrap(text: any, width: number) {
    text.each(function(this: any) {
      const text = d3.select(this);
      const words = text.text().split(/\s+/).reverse();
      let word;
      let line: string[] = [];
      let lineNumber = 0;
      const lineHeight = 1.1;
      const y = text.attr('y');
      const dy = parseFloat(text.attr('dy'));
      let tspan = text.text(null).append('tspan').attr('x', 0).attr('y', y).attr('dy', dy + 'em');
      
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(' '));
        if (tspan.node()!.getComputedTextLength() > width) {
          line.pop();
          tspan.text(line.join(' '));
          line = [word];
          tspan = text.append('tspan').attr('x', 0).attr('y', y).attr('dy', ++lineNumber * lineHeight + dy + 'em').text(word);
        }
      }
    });
  }

  exportVisualization(): void {
    const svgData = this.svg.node().outerHTML;
    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const svgUrl = URL.createObjectURL(svgBlob);
    
    const downloadLink = document.createElement('a');
    downloadLink.href = svgUrl;
    downloadLink.download = `d3-visualization-${Date.now()}.svg`;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  }

  resetVisualization(): void {
    this.updateVisualization();
  }

  getVisualizationTitle(): string {
    const titles: { [key: string]: string } = {
      'force-directed': 'Grafo de Fuerza Dirigida',
      'treemap': 'Mapa de Árbol',
      'sankey': 'Diagrama Sankey',
      'heatmap': 'Mapa de Calor',
      'network': 'Red de Conexiones'
    };
    return titles[this.selectedVisualization()] || 'Visualización D3.js';
  }

  getDataInfo(): string {
    return `${this.data.length} elementos, ${this.selectedDataset()}`;
  }

  getDataSummary() {
    const total = this.data.reduce((sum, d) => sum + d.value, 0);
    const categories = [...new Set(this.data.map(d => d.category))];
    const max = Math.max(...this.data.map(d => d.value));
    const min = Math.min(...this.data.map(d => d.value));

    return [
      { label: 'Total de Elementos', value: this.data.length },
      { label: 'Valor Total', value: total },
      { label: 'Categorías', value: categories.length },
      { label: 'Valor Máximo', value: max },
      { label: 'Valor Mínimo', value: min }
    ];
  }
}
