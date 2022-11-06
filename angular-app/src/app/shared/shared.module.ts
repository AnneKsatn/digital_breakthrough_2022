import { NgModule } from '@angular/core';
// import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
// import { OrderListModule } from 'primeng/orderlist';
import { InputTextModule } from 'primeng/inputtext';
// import { ToolbarModule } from 'primeng/toolbar';
// import { SplitButtonModule } from 'primeng/splitbutton';
import { ButtonModule } from 'primeng/button';
// import { TableModule } from 'primeng/table';
// import { DropdownModule } from 'primeng/dropdown';
// import { MultiSelectModule } from 'primeng/multiselect';
// import { SliderModule } from 'primeng/slider';
// import { ProgressBarModule } from 'primeng/progressbar';
// import { TabViewModule } from 'primeng/tabview';
// import { CalendarModule } from 'primeng/calendar';
// import { TimelineModule } from 'primeng/timeline';
// import { CardModule } from 'primeng/card';
// import { DialogModule } from 'primeng/dialog';
// import { InputTextareaModule } from 'primeng/inputtextarea';
// import { FileUploadModule } from 'primeng/fileupload';



@NgModule({
  declarations: [],
  imports: [
    // BrowserAnimationsModule,
    // OrderListModule,
    // InputTextModule,
    // ToolbarModule,
    // SplitButtonModule,
    ButtonModule,
    // TableModule,
    // DropdownModule,
    // MultiSelectModule,
    // SliderModule,
    // ProgressBarModule,
    // TabViewModule,
    // CalendarModule,
    // TimelineModule,
    // CardModule,
    // DialogModule,
    // InputTextareaModule,
    // FileUploadModule,
  ],
  exports: [
    // BrowserAnimationsModule,
    // OrderListModule,
    InputTextModule,
    // ToolbarModule,
    // SplitButtonModule,
    ButtonModule,
    // TableModule,
    // DropdownModule,
    // MultiSelectModule,
    // SliderModule,
    // ProgressBarModule,
    // TabViewModule,
    // CalendarModule,
    // TimelineModule,
    // CardModule,
    // DialogModule,
    // InputTextareaModule,
    // FileUploadModule,
  ],
})
export class SharedModule { }
