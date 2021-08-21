import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StatsComponent } from './stats/stats.component'
import { PlanComponent } from './plan/plan.component'

const routes: Routes = [
  { path: 'stats', component: StatsComponent },
  { path: 'plan', component: PlanComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
