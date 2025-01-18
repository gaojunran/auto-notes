import request from "./request.ts";

export interface RecordResponse {
    id: number;
    duration: number;
    topic: string;
    abstract: string;
    raw_recognition: string;
}

export interface NoteRequest {
    topic: string;
    raw_recognition: string;
}

export interface NoteResponse {
    notes: string;
}

export interface ThoughtRequest {
    notes: string;
    num: number;
}

export interface Question {
    question: string | string[];
    answer: string;
    analysis?: string;
    knowledge?: string[];
}

export interface ThoughtResponse {
    questions: Question[];
}

export interface ExerciseRequest {
    notes: string;
    num: number;
}

export interface ExerciseResponse {
    questions: Question[];
}

export const testConnection = async () => {
    const response = await request("/test", "GET")
    return response === "Hello, World!";
}

export const postRecord = async (record: FormData)=> {
    const response: RecordResponse = await request("/record", "POST", record,{
        'Content-Type': "multipart/form-data; boundary=--------------------------061678868844241685450298",
        "Accept": "*/*"})
    return response;
}

export const getNote = async (note: NoteRequest)=> {
    const response: NoteResponse = await request("/note", "POST", note)
    return response;
}

export const getThought = async (thought: ThoughtRequest)=> {
    const response: ThoughtResponse = await request("/thought", "POST", thought)
    return response;
}

export const getExercise = async (exercise: ExerciseRequest)=> {
    const response: ExerciseResponse = await request("/exercise", "POST", exercise)
    return response;
}

