import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('firma-frontend');
}
saludar() {
  alert('Hola Felipe, ya estamos trabajando con Angular moderno 🚀');
}