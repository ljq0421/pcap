package org.fkjava.mavenqs.service.inter;
import org.fkjava.mavenqs.entity.Insuser;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InsuserService {
    List<Insuser> getProject();
    List<Insuser> getVM(String project);
    List<Insuser> getPast(String pastshow,String displayname);
    List<Insuser> getPastAll(String displayname);
    List<Insuser> getName(String project);
    List<Insuser> getRule();
    List<Insuser> getRuleByRuleId(String ruleid);
    List<Insuser> getPastByRuleId(String ruleid);
    int makeRule(String ruleinfo, Insuser insuser);
    int deleteRule(String rulename,String ruleobject,String ruleinfo,String rulestate, Insuser insuser);
}

