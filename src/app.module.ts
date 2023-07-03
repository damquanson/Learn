import { Module } from '@nestjs/common';
import { LaptopsController } from './app.controller';
import {  LaptopsService } from './app.service';
import { LaptopsModule } from './laptops/laptops.module';

@Module({
  imports: [LaptopsModule],
  controllers: [LaptopsController],
  providers: [LaptopsService],
})
export class AppModule {}
