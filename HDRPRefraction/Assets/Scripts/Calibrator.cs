using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System.IO;

public class Calibrator : MonoBehaviour
{
    public Camera mainCamera;
    public int waitingFrames;
    public GameObject plane;
    public bool isTrain;
    public int startImageIndex = 0;

    private ImageSynthesis imageSynthesis;
    private string materialFormat;
    private int count;
    private int waitingCounter;
    private Recorder recorder;
    private List<GameObject> prefabs;

    void Start()
    {
        imageSynthesis = mainCamera.GetComponent<ImageSynthesis>();
        materialFormat = "graycode_512_512/Materials/graycode_";
        count = 1;
        waitingCounter = 0;
        recorder = new Recorder();
        prefabs = new List<GameObject>();
        // recorder.ParseFile("train/recorder/record_10.txt");
        // recorder.Show();
    }

    void FixedUpdate()
    {
        // if (count > 18)
        //     count = 1;
        // if (waitingCounter == 0)
        // {
        //     Material graycode = Resources.Load(materialFormat + count.ToString(), typeof(Material)) as Material;
        //     plane.GetComponent<MeshRenderer>().material = graycode;
        // }
        // if (waitingCounter == waitingFrames)
        // {
        //     imageSynthesis.Save(string.Format("debug{0}.png", count), 512, 512, "", 0);
        //     count += 1;
        //     waitingCounter = -1;
        // }
        // waitingCounter += 1;
        // print(waitingFrames);
    }

    GameObject LoadPrefab(string path)
    {
        GameObject prefab = AssetDatabase.LoadAssetAtPath(path, typeof(GameObject)) as GameObject;
        if (prefab == null)
        {
            print(path);
        }

        return Instantiate(prefab);
    }

    Material LoadGlassMaterial(int idx, float IOR)
    {
        string materialPath = "GlassMaterials/Glass" + idx.ToString();
        Material material = Resources.Load(materialPath, typeof(Material)) as Material;
        material.SetFloat("_Ior", IOR);

        return material;
    }

    void MakeDirectory(string path)
    {
        DirectoryInfo info = new DirectoryInfo(path);
        if (!info.Exists)
        {
            info.Create();
        }
    }
}
