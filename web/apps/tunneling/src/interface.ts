export interface SingleFile {
  data: any;
  type: string;
}

export interface MultiFile {
  [filename: string]: SingleFile;
}
