import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomePageComponent } from './home-page/home-page.component';
import { SystemComponent } from './system.component';

const routes: Routes = [
  {
    path: 'system', component: SystemComponent, children: [
      {
        path: 'home-page', component: HomePageComponent, children: [
        ]
      }
    ]
  }]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class SystemRoutingModule { }
