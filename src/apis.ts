import request from "./request.ts";
import {Point, RawRecognition} from "./types.ts";

export interface RecordResponse {
    /**
     * 课程摘要，长度大约为2行。
     */
    abstract: string;
    /**
     * 课程时长，单位为秒。
     */
    duration: number;
    /**
     * id，课程的唯一id。可以随机生成但不能重复。
     */
    id: number;
    /**
     * 原始转文字结果
     */
    raw_recognition: RawRecognition[];
    /**
     * 课程主题，限制长度不能超过10个字。
     */
    topic: string;
    [property: string]: any;
}

export interface NoteRequest {
    /**
     * 课程摘要
     */
    abstract: string;
    raw_recognition: RawRecognition;
    /**
     * 课程主题
     */
    topic: string;
    [property: string]: any;
}

export interface NoteResponse {
    /**
     * 多个知识点
     */
    points: Point[];
    [property: string]: any;
}

// export interface ThoughtRequest {
//     notes: string;
//     num: number;
// }
//
// export interface Question {
//     question: string | string[];
//     answer: string;
//     analysis?: string;
//     knowledge?: string[];
// }
//
// export interface ThoughtResponse {
//     questions: Question[];
// }
//
// export interface ExerciseRequest {
//     notes: string;
//     num: number;
// }
//
// export interface ExerciseResponse {
//     questions: Question[];
// }

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

// export const getThought = async (thought: ThoughtRequest)=> {
//     const response: ThoughtResponse = await request("/thought", "POST", thought)
//     return response;
// }
//
// export const getExercise = async (exercise: ExerciseRequest)=> {
//     const response: ExerciseResponse = await request("/exercise", "POST", exercise)
//     return response;
// }

