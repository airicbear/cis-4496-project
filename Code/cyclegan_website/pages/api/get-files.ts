import fs from "fs";
import { NextApiRequest, NextApiResponse } from "next";
import path from "path";

type Data = {
  files: string[];
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const { dir } = req.query;
  if (dir) {
    const dirPath = path.join(process.cwd(), "public", dir as string);

    try {
      const files = fs.readdirSync(dirPath);
      res.status(200).json({ files });
    } catch (error) {
      console.error(error);
      res.status(500).json({ files: [] });
    }
  } else {
    res.status(500).json({ files: [] });
  }
}
