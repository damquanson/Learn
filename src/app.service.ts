import { Injectable } from '@nestjs/common';
import * as fs from 'fs';
import * as csvParser from 'csv-parser';

@Injectable()
export class LaptopsService {
  async readCsvFile(filePath: string, page: number, pageSize: number): Promise<any[]> {
    return new Promise((resolve, reject) => {
      const laptops: any[] = [];
      let skippedRecords = (page - 1) * pageSize;
      let processedRecords = 0;
  
      fs.createReadStream(filePath)
        .pipe(csvParser())
        .on('data', (data: any) => {
          if (processedRecords >= skippedRecords && laptops.length < pageSize) {
            laptops.push(data);
          }
          processedRecords++;
        })
        .on('end', () => resolve(laptops))
        .on('error', (error: any) => reject(error));
    });
  }
  
  async searchLaptopsByName(name: string,page:number): Promise<any[]> {
    const filePath = 'final.csv'; 
    const laptops = await this.readCsvFile(filePath,page,20);
  
    const filteredLaptops = laptops.filter(laptop => laptop.Name.toLowerCase().includes(name.toLowerCase()));
    return filteredLaptops;
  }
  async filterBySource(data: any[], source: string): Promise<any[]> {
    return data.filter((item) => item.Source === source);
  }

  
}
