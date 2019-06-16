package org.fkjava.mavenqs.service.impl;

import org.fkjava.mavenqs.dao.InsuserDao;
import org.fkjava.mavenqs.entity.Insuser;
import org.fkjava.mavenqs.service.inter.InsuserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class InsuserServiceImpl implements InsuserService {
    @Autowired
    private InsuserDao insuserDao;
    @Override
    public List<Insuser> getProject() {
        return insuserDao.getProject();
    }
    @Override
    public List<Insuser> getVM(String project) {
        return insuserDao.getVM(project);
    }
    @Override
    public List<Insuser> getPast(String pastshow,String displayname) {
        return insuserDao.getPast(pastshow,displayname);
    }
    @Override
    public List<Insuser> getPastAll(String displayname) {
        return insuserDao.getPastAll(displayname);
    }
    @Override
    public List<Insuser> getName(String project) {
        return insuserDao.getName(project);
    }
    @Override
    public List<Insuser> getRule() {
        return insuserDao.getRule();
    }
    @Override
    public List<Insuser> getRuleByRuleId(String ruleid) {
        return insuserDao.getRuleByRuleId(ruleid);
    }
    @Override
    public List<Insuser> getPastByRuleId(String ruleid) {
        return insuserDao.getPastByRuleId(ruleid);
    }
    @Override
    public int makeRule(String ruleinfo,Insuser insuser) {
        return insuserDao.makeRule(ruleinfo,insuser);
    }
    @Override
    public int deleteRule(String rulename,String ruleobject,String ruleinfo,String rulestate,Insuser insuser) {
        return insuserDao.deleteRule(rulename,ruleobject,ruleinfo,rulestate,insuser);
    }
}

