import axios from 'axios';
import { Person, PersonCreate, PersonUpdate } from '../types/interfaces';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const peopleApi = {
  getAll: async (): Promise<Person[]> => {
    const response = await api.get<Person[]>('/people');
    return response.data;
  },

  getById: async (id: number): Promise<Person> => {
    const response = await api.get<Person>(`/people/${id}`);
    return response.data;
  },

  create: async (person: PersonCreate): Promise<Person> => {
    const response = await api.post<Person>('/people', person);
    return response.data;
  },

  update: async (id: number, person: PersonUpdate): Promise<Person> => {
    const response = await api.put<Person>(`/people/${id}`, person);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/people/${id}`);
  },
};