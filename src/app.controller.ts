import { Controller, Get, Param, ParseIntPipe, Query } from '@nestjs/common';
import { LaptopsService } from './app.service';

 export const filePath="final.csv"
@Controller('laptops')
export class LaptopsController {
  constructor(private readonly laptopsService: LaptopsService) {}
  @Get('filter')
  async getFptRecords(@Query('source') source:string,@Query('page') page:number=1): Promise<any[]> {
    const data = await this.laptopsService.readCsvFile(filePath,1,2000);
    
    const laptopSmall = await this.laptopsService.filterBySource(data, source,page);
    
    const laptopFull =await this.laptopsService.readCsvFile(filePath,1,2000);
    laptopSmall.forEach((smallLaptop) => {
      smallLaptop.matching = laptopFull
        .filter((fullLaptop) =>
          fullLaptop['Matching Group'] === smallLaptop['Matching Group'] &&
          fullLaptop['Source'] !== smallLaptop['Source']
        );
    });
    return laptopSmall;
  }
  @Get()
  async getAllLaptops(@Query('page') page:number=1): Promise<any[]> {
    const laptopFull =await this.laptopsService.readCsvFile(filePath,1,2000);
    const laptopSmall = await this.laptopsService.readCsvFile(filePath,page,10);
    laptopSmall.forEach((smallLaptop) => {
      smallLaptop.matching = laptopFull
        .filter((fullLaptop) =>
          fullLaptop['Matching Group'] === smallLaptop['Matching Group'] &&
          fullLaptop['Source'] !== smallLaptop['Source']
        );
    });
    
    return laptopSmall;
  }
  @Get('search')
  async searchLaptopsByName(@Query('name') name: string,@Query('page') page:number=1): Promise<any[]> {
    const laptopSmall = await this.laptopsService.searchLaptopsByName(name,page);
    const laptopFull =await this.laptopsService.readCsvFile(filePath,1,2000);
    laptopSmall.forEach((smallLaptop) => {
      smallLaptop.matching = laptopFull
        .filter((fullLaptop) =>
          fullLaptop['Matching Group'] === smallLaptop['Matching Group'] &&
          fullLaptop['Source'] !== smallLaptop['Source']
        );
    });
    return laptopSmall;

  }
}
