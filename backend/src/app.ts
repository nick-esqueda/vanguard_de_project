import express, { Application, Request, Response, NextFunction } from "express";
const app: Application = express();

const add = (x: number, y: number): number => x + y;

app.get("/", (req: Request, res: Response, next: NextFunction) => {
    console.log(add(3, 4));
    res.send("hello");
});


app.listen(5000, () => console.log("SERVER IS NOW RUNNING."));