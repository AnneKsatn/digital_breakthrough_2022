import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomePageComponent } from './home-page/home-page.component';
import { SystemRoutingModule } from './system-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { MultiSelectModule } from 'primeng/multiselect';
import { SystemComponent } from './system.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { InputNumberModule } from 'primeng/inputnumber';


@NgModule({
  declarations: [
    HomePageComponent,
    SystemComponent
  ],
  imports: [
    CommonModule,
    SystemRoutingModule,
    HttpClientModule,
    MultiSelectModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    InputNumberModule
  ]
})
export class SystemModule { }
