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
    const laptops = await this.readCsvFile(filePath,1,2000);
  
    const filteredLaptops = laptops.filter(laptop => laptop.Name.toLowerCase().includes(name.toLowerCase()));
    return this.paginateArray(filteredLaptops,20,page);
  }
  async filterBySource(data: any[], source: string,page:number): Promise<any[]> {
    var filteredObjects = [];
    
for (var i = 0; i < data.length; i++) {
  
  if (data[i].Source === source  ) {
    filteredObjects.push(data[i]);
  }
}
return this.paginateArray(filteredObjects,20,page)
  }


  paginateArray(array, itemsPerPage, pageNumber) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    
    return array.slice(startIndex, endIndex);
  }
}
