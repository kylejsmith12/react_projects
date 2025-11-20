export interface Person {
  id?: number;
  first_name: string;
  last_name: string;
  occupation: string;
}

export interface PersonCreate {
  first_name: string;
  last_name: string;
  occupation: string;
}

export interface PersonUpdate {
  first_name?: string;
  last_name?: string;
  occupation?: string;
}