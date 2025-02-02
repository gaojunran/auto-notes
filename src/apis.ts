import request from "./request.ts";
import {NodeCategory, NodeLink, Node, Point, RawRecognition, Lecture} from "./types.ts";

export interface StateResponse {
    response: string;
    [property: string]: any;
}

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
    raw_recognition: RawRecognition[];
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

export interface NetworkRequest {
    lectures: Lecture[];
    [property: string]: any;
}

export interface NetworkResponse {
    /**
     * 节点类别, 注意：每个topic为一个category。
     */
    categories: NodeCategory[];
    /**
     * 节点链接, 注意：topic节点和其子point节点之间需要建立链接、各point之间也可以建立链接。
     */
    links: NodeLink[];
    /**
     * 节点, 注意：课程主题topic和课程的所有知识点point都会作为节点。
     */
    nodes: Node[];
    [property: string]: any;
}

export interface ExportRequest {
    id: number;
    topic: string;
    abstract: string;

    points: Point[];

    [property: string]: any;
}



export const testConnection = async () => {
    const response = (await request("/test", "GET")) as StateResponse;
    return response.response === "OK";
}

export const postRecord = async (record: FormData) => {
    const response = await request("/record", "POST", null, record, {})  // headers will be auto-generated
    return response as RecordResponse;
}

export const getNote = async (note: NoteRequest) => {
    const response = await request("/note", "POST", note)
    return response as NoteResponse;
}

export const getNetwork = async (req: NetworkRequest) => {
    const response = await request("/network", "POST", req)
    return response as NetworkResponse;
}

export const getExport = async (req: ExportRequest) => {
    const response = (await request("/export", "POST", req)) as StateResponse;
    return response.response === "OK";
}

