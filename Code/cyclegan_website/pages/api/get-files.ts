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
  const { dir, limit = 10, offset = 0 } = req.query;
  if (dir) {
    const dirPath = path.join(process.cwd(), "public", dir as string);

    try {
      const filenames = fs.readdirSync(dirPath);
      const startIndex = parseInt(offset as string, 10);
      const endIndex = startIndex + parseInt(limit as string, 10);
      const files = filenames.slice(startIndex, endIndex);
      res.status(200).json({ files });
    } catch (error) {
      console.error(error);
      res.status(500).json({ files: [] });
    }
  } else {
    res.status(500).json({ files: [] });
  }
}
